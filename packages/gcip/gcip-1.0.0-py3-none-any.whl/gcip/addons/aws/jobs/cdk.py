import warnings
from typing import Dict, List, Optional
from dataclasses import field, dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)


@dataclass
class BootstrapOpts:
    aws_account_id: str
    aws_region: str
    toolkit_stack_name: str
    qualifier: str
    resource_tags: Optional[Dict[str, str]] = None
    job_opts: Optional[JobOpts] = None


class Bootstrap(Job):
    def __init__(
        self,
        *,
        aws_account_id: str,
        aws_region: str,
        toolkit_stack_name: str,
        qualifier: str,
        resource_tags: Optional[Dict[str, str]] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `toolkit-stack`
            * `job_opts.stage` defaults to `deploy`
              contain the `crane` binary.
        """

        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "toolkit-stack"
        if not job_opts.stage:
            job_opts.stage = "deploy"

        script = [
            "cdk bootstrap",
            f"--toolkit-stack-name {toolkit_stack_name}",
            f"--qualifier {qualifier}",
            f"aws://{aws_account_id}/{aws_region}",
        ]

        if resource_tags:
            script.extend([f"-t {k}={v}" for k, v in resource_tags.items()])

        job_opts.script = " ".join(script)

        super().__init__(**job_opts.__dict__)
        self.add_variables(CDK_NEW_BOOTSTRAP="1")


@dataclass
class DeployOpts:
    stacks: List[str] = field(default_factory=list)
    toolkit_stack_name: Optional[str] = None
    strict: bool = True
    wait_for_stack: bool = True
    wait_for_stack_assume_role: Optional[str] = None
    wait_for_stack_account_id: Optional[str] = None
    deploy_options: Optional[str] = None
    context: Optional[Dict[str, str]] = None
    job_opts: Optional[JobOpts] = None


class Deploy(Job):
    def __init__(
        self,
        *,
        stacks: List[str],
        toolkit_stack_name: Optional[str] = None,
        strict: bool = True,
        wait_for_stack: bool = True,
        wait_for_stack_assume_role: Optional[str] = None,
        wait_for_stack_account_id: Optional[str] = None,
        deploy_options: Optional[str] = None,
        context: Optional[Dict[str, str]] = None,
        job_opts: Optional[JobOpts] = None,
    ):
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "cdk"
        if not job_opts.stage:
            job_opts.stage = "deploy"

        job_opts.script = []

        stacks_string = " ".join(stacks)
        script = ["cdk deploy --require-approval 'never'"]

        if strict:
            script.append("--strict")

        if deploy_options:
            script.append(deploy_options)

        if context:
            script.extend([f"-c {k}={v}" for k, v in context.items()])

        script.append(f"--toolkit-stack-name {toolkit_stack_name}")
        script.append(stacks_string)

        if wait_for_stack:
            wait_for_stack_options = ""
            if wait_for_stack_assume_role:
                wait_for_stack_options += f" --assume-role {wait_for_stack_assume_role}"
                if wait_for_stack_account_id:
                    wait_for_stack_options += f" --assume-role-account-id {wait_for_stack_account_id}"
            elif wait_for_stack_account_id:
                warnings.warn("`wait_for_stack_account_id` has no effects without `wait_for_stack_assume_role`")

            job_opts.script.extend(
                [
                    "pip3 install gcip",
                    f"python3 -m gcip.addons.aws.tools.wait_for_cloudformation_stack_ready --stack-names '{stacks_string}'{wait_for_stack_options}",
                ]
            )

        job_opts.script.append(" ".join(script))

        super().__init__(**job_opts.__dict__)


@dataclass
class DiffOpts:
    stacks: List[str] = field(default_factory=list)
    diff_options: Optional[str] = None
    context: Optional[Dict[str, str]] = None
    job_opts: Optional[JobOpts] = None


class Diff(Job):
    def __init__(
        self,
        *,
        stacks: List[str],
        diff_options: Optional[str] = None,
        context: Optional[Dict[str, str]] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:

        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "cdk"
        if not job_opts.stage:
            job_opts.stage = "diff"

        script = ["cdk diff"]
        if diff_options:
            script.append(diff_options)

        if context:
            script.extend([f"-c {k}={v}" for k, v in context.items()])

        script.append(" ".join(stacks))

        job_opts.script = " ".join(script)

        super().__init__(**job_opts.__dict__)
