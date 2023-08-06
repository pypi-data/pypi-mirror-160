import os
import subprocess
from typing import Dict, List, Optional
from .exceptions import LoggedError


class TerraformError(LoggedError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Terraform:
    def __init__(self, directory: Optional[str] = None) -> None:
        if directory and not os.path.exists(directory):
            raise TerraformError(
                f"Can't find directory '{directory}'. Are you at the root of the project?"
            )
        env = os.environ.copy()
        env["TF_IN_AUTOMATION"] = "true"
        self.env = env
        self.dir = directory
        self.exe = "terraform"
        self._run("init")

    def select_workspace(self, workspace: str) -> None:
        self._run("workspace", "select", workspace)
        self.workspace = workspace

    def plan(
        self,
        out: str,
        vars: Optional[Dict[str, str]] = None,
        refresh_only: bool = False,
    ) -> None:
        subcmd = [
            "plan",
            f"-var-file=.{self.workspace}.tfvars",
            f"-out={out}",
        ]
        if vars:
            subcmd.extend([f"-var={k}={v}" for k, v in vars.items()])
        if refresh_only:
            subcmd.append("-refresh-only")
        self._run(*subcmd)

    def apply(self, planfile: str) -> None:
        self._run("apply", planfile)

    def _run(self, *subcmd: str) -> None:
        try:
            cmd = [self.exe] + list(subcmd)
            subprocess.run(cmd, cwd=self.dir, env=self.env, check=True)
        except subprocess.CalledProcessError:
            raise TerraformError(
                "An error occured in terraform. Please see above error message."
            )
