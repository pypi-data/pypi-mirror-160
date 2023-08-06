from typing import Optional
from warnings import warn
from dataclasses import dataclass

from gcip.core.variables import PredefinedVariables
from gcip.addons.git.jobs.git import Mirror, MirrorOpts
from gcip.addons.linux.scripts.package_manager import (
    install_packages,
)


@dataclass
class MirrorToCodecommitOpts:
    repository_name: Optional[str]
    aws_region: Optional[str] = None
    infrastructure_tags: Optional[str] = None
    mirror_opts: Optional[MirrorOpts] = None


class MirrorToCodecommit(Mirror):
    def __init__(
        self,
        *,
        repository_name: Optional[str] = None,
        aws_region: Optional[str] = None,
        infrastructure_tags: Optional[str] = None,
        mirror_opts: Optional[MirrorOpts] = None,
    ) -> None:
        """
        This job clones the CI_COMMIT_REF_NAME of the current repository and forcefully pushes this REF to a AWS CodeCommit repository.

        This job requires following IAM permissions:

            - codecommit:CreateRepository
            - codecommit:GetRepository
            - codecommit:CreateBranch
            - codecommit:GitPush
            - codecommit:TagResource

        You could also limit the resource to `!Sub arn:aws:codecommit:${AWS::Region}:${AWS::AccountId}:<repository-name>`.

        Args:
            repository_name (Optional str): The name of the target Codecommit repository. Defaults to CI_PROJECT_PATH_SLUG.
            aws_region (Optional str): The AWS region you want to operate in. When not set, it would be curl'ed from the current
                EC2 instance metadata.
            infrastructure_tags (Optional str): Only if the ECR would be created on the first call, these AWS Tags becomes applied to
              the AWS Codecommit resource. Changed values won't change the tags on an already existing ECR. This string must have the
              pattern: `Tag1=Value1,Tag2=Value2`
            mirror_opts (Optional[MirrorOpts]): Options for the upstream git.Mirror job.
        """

        if not mirror_opts:
            mirror_opts = MirrorOpts()

        if mirror_opts.remote_repository:
            warn("mirror_opts.remote_repository will be overridden by MirrorToCodecommit")
        mirror_opts.remote_repository = "${GCIP_REMOTE_REPO_URL}"

        if not repository_name:
            repository_name = PredefinedVariables.CI_PROJECT_PATH_SLUG

        infrastructure_tags_option = ""
        if infrastructure_tags:
            infrastructure_tags_option = f'--tags "{infrastructure_tags}"'

        if mirror_opts.script_hook is None:
            mirror_opts.script_hook = []

        if aws_region:
            mirror_opts.script_hook.append(f"export AWS_DEFAULT_REGION={aws_region}")
        else:
            mirror_opts.script_hook.extend(
                [
                    install_packages("curl", "jq"),
                    "export AWS_DEFAULT_REGION=$(curl --silent http://169.254.169.254/latest/dynamic/instance-identity/document | jq -r .region)",
                ]
            )

        get_repo_url_string = (
            f'GCIP_REMOTE_REPO_URL=$(aws codecommit get-repository --repository-name "{repository_name}" --output text'
            " --query repositoryMetadata.cloneUrlHttp"
            f' || aws codecommit create-repository --repository-name "{repository_name}" {infrastructure_tags_option} --output text'
            " --query repositoryMetadata.cloneUrlHttp)"
        )

        mirror_opts.script_hook.extend(
            [
                install_packages("aws-cli"),
                get_repo_url_string,
                "git config --local credential.helper '!aws codecommit credential-helper $@'",
                "git config --local credential.UseHttpPath true",
            ]
        )

        super().__init__(**mirror_opts.__dict__)
