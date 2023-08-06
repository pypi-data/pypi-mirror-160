from typing import List, Optional
from dataclasses import dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)
from gcip.core.rule import Rule
from gcip.core.variables import PredefinedVariables
from gcip.addons.container.images import PredefinedImages


@dataclass
class MirrorOpts:
    remote_repository: Optional[str] = None
    git_config_user_email: Optional[str] = None
    git_config_user_name: Optional[str] = None
    private_key_variable: Optional[str] = None
    script_hook: Optional[List[str]] = None
    run_only_for_repository_url: Optional[str] = None
    job_opts: Optional[JobOpts] = None


class Mirror(Job):
    def __init__(
        self,
        *,
        remote_repository: str,
        git_config_user_email: Optional[str] = None,
        git_config_user_name: Optional[str] = None,
        private_key_variable: Optional[str] = None,
        script_hook: Optional[List[str]] = None,
        run_only_for_repository_url: Optional[str] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        This job clones the CI_COMMIT_REF_NAME of the current repository and forcefully pushes this REF to the `remote_repository`.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `git-mirror`
            * `job_opts.stage` defaults to `deploy`
               contain the `git` binary.

        Args:
            remote_repository (str): The git repository the code of the pipelines repository should be mirrored to.
            git_config_user_email (Optional str): The 'user.email' with which the commits to the remote repository
                should be made. Defaults to GITLAB_USER_EMAIL.
            git_config_user_name (Optional str): The 'user.name' with which the commits to the remote repository
                should be made. Defaults to GITLAB_USER_NAME.
            private_key_variable (Optional str): DO NOT PROVIDE YOUR PRIVATE SSH KEY HERE!!! This parameter takes
                the name of the Gitlab environment variable, which contains the private ssh key used to push to the
                remote repository. This one should be created as protected and masked variable in the 'CI/CD' settings
                of your project.
            script_hook (Optional List(str)): This list of strings could contain any commands that should be executed
                between pulling the current repository and pushing it to the remote. This hook is mostly meant to be
                for git configuration commands, required to push to the remote repository.
            run_only_for_repository_url (Optional[str]): When mirroring to a remote Gitlab instance, you don't want to
                run this mirroring job there again. With this variable the job only runs, when its value matches
                the CI_REPOSITORY_URL of the current repository.
        """

        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "git-mirror"
        if not job_opts.stage:
            job_opts.stage = "deploy"
        if not job_opts.image:
            job_opts.image = PredefinedImages.ALPINE_GIT

        if not git_config_user_email:
            git_config_user_email = PredefinedVariables.GITLAB_USER_EMAIL
        if not git_config_user_name:
            git_config_user_name = PredefinedVariables.GITLAB_USER_NAME
        if not script_hook:
            script_hook = []

        job_opts.script = []

        if private_key_variable:
            job_opts.script.extend(
                # this will start the ssh-agent and temporarily
                # add the ssh private key to it
                [
                    "eval $(ssh-agent -s)",
                    f"""echo "${private_key_variable}" | tr -d '\\r' | ssh-add - > /dev/null""",
                ]
            )

        job_opts.script.extend(
            [
                "set -eo pipefail",
                "mkdir /tmp/repoReplicaUniqueDir",
                "cd /tmp/repoReplicaUniqueDir",
                f"git clone -b {PredefinedVariables.CI_COMMIT_REF_NAME} {PredefinedVariables.CI_REPOSITORY_URL} .",
                f'git config --global user.email "{git_config_user_email}"',
                f'git config --global user.name "{git_config_user_name}"',
                *script_hook,
                f"git push --force {remote_repository} {PredefinedVariables.CI_COMMIT_REF_NAME}:{PredefinedVariables.CI_COMMIT_REF_NAME}",
                f'echo "Published code to {remote_repository}:{PredefinedVariables.CI_COMMIT_REF_NAME}"',
            ]
        )

        if run_only_for_repository_url:
            if not job_opts.rules:
                job_opts.rules = []
            job_opts.rules.append(Rule(if_statement=f'CI_REPOSITORY_URL="{run_only_for_repository_url}"'))

        super().__init__(**job_opts.__dict__)
