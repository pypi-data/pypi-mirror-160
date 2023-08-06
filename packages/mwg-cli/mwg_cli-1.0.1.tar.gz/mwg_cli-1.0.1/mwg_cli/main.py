import os
from argparse import ArgumentParser, Namespace

from . import git, plans
from .plans import PlanNotFound
from .build import build
from .terraform import Terraform
from .exceptions import LoggedError

TF_DIR = "tf"


def main() -> None:
    try:
        git.ensure_repo()

        parser = ArgumentParser()

        subparsers = parser.add_subparsers(title="actions")

        deployment_parser = ArgumentParser(add_help=False)
        deployment_parser.add_argument(
            "workspace",
            help="The Terraform workspace to select before planning or applying. Usually dev, qa, or prod.",
        )

        parser_plan = subparsers.add_parser(
            "plan",
            parents=[deployment_parser],
            help="Create and upload an execution plan based on the current head commit",
        )
        parser_plan.add_argument(
            "--refresh-only",
            action="store_true",
            help="Only refresh state",
        )
        parser_plan.set_defaults(func=plan)

        parser_apply = subparsers.add_parser(
            "apply",
            parents=[deployment_parser],
            help="Apply the execution plan for the current head commit",
        )
        parser_apply.set_defaults(func=apply)

        args = parser.parse_args()

        if not hasattr(args, "func"):
            parser.print_help()
            return

        args.func(args)

    except LoggedError as e:
        print(e)


def plan(args: Namespace):
    git.ensure_clean_working_tree()
    head = git.get_head()
    if os.path.exists("cloudbuild.yaml"):
        build(substitutions=dict(SHORT_SHA=head.sha))
    tf = Terraform(TF_DIR)
    tf.select_workspace(args.workspace)
    tf.plan(
        out=head.sha,
        vars=dict(commit_sha=head.sha),
        refresh_only=args.refresh_only,
    )
    planfile = _planfile(head.sha)
    plans.upload(args.workspace, planfile)
    os.remove(planfile)


def apply(args: Namespace) -> None:
    git.unshallow()
    head = git.get_head()
    try:
        planfile = _planfile(head.sha)
        plans.download(args.workspace, planfile)
        print("Could not find plan for head commit")
    except PlanNotFound:
        print("Checking for an empty merge")
        if head.second_parent and head.is_empty_merge:
            planfile = _planfile(head.second_parent)
            plans.download(args.workspace, planfile)
        else:
            print("Commit is not an empty merge, re-raising")
            raise
    tf = Terraform(TF_DIR)
    tf.select_workspace(args.workspace)
    tf.apply(os.path.basename(planfile))


def _planfile(sha: str) -> str:
    return os.path.join(TF_DIR, sha)
