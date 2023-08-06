from typing import Dict, List, Optional
from warnings import warn
from dataclasses import dataclass

from gcip.core.sequence import Sequence
from gcip.addons.aws.jobs.cdk import (
    Diff,
    Deploy,
    DiffOpts,
    DeployOpts,
)


@dataclass
class DiffDeployOpts:
    stacks: List[str]
    context: Optional[Dict[str, str]] = None
    cdk_diff_opts: Optional[DiffOpts] = None
    cdk_deploy_opts: Optional[DeployOpts] = None


class DiffDeploy(Sequence):
    def __init__(
        self,
        *,
        stacks: List[str],
        context: Optional[Dict[str, str]] = None,
        cdk_diff_opts: Optional[DiffOpts] = None,
        cdk_deploy_opts: Optional[DeployOpts] = None,
    ) -> None:

        super().__init__()

        #
        # cdk diff
        #

        if not cdk_diff_opts:
            cdk_diff_opts = DiffOpts()

        if cdk_diff_opts.stacks:
            warn("cdk_diff_opts.stacks will be overridden by DiffDeploy.stacks")
        if cdk_diff_opts.context:
            warn("cdk_diff_opts.context will be overridden by DiffDeploy.context")

        cdk_diff_opts.stacks = stacks
        cdk_diff_opts.context = context

        self.diff_job = Diff(**cdk_diff_opts.__dict__)

        #
        # cdk deploy
        #

        if not cdk_deploy_opts:
            cdk_deploy_opts = DeployOpts()
        cdk_deploy_opts = cdk_deploy_opts

        if cdk_deploy_opts.stacks:
            warn("cdk_deploy_opts.stacks will be overridden by DiffDeploy.stacks")
        if cdk_deploy_opts.context:
            warn("cdk_deploy_opts.context will be overridden by DiffDeploy.context")

        cdk_deploy_opts.stacks = stacks
        cdk_deploy_opts.context = context

        self.deploy_job = Deploy(**cdk_deploy_opts.__dict__)
        self.deploy_job.add_needs(self.diff_job)

        self.add_children(
            self.diff_job,
            self.deploy_job,
        )
