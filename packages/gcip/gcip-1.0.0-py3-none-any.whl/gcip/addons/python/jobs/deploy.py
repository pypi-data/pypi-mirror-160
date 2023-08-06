from typing import Optional
from dataclasses import dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)


@dataclass
class TwineUploadOpts:
    twine_repository_url: Optional[str] = None
    twine_username_env_var: Optional[str] = "TWINE_USERNAME"
    twine_password_env_var: Optional[str] = "TWINE_PASSWORD"
    job_opts: Optional[JobOpts] = None


class TwineUpload(Job):
    def __init__(
        self,
        *,
        twine_repository_url: Optional[str] = None,
        twine_username_env_var: Optional[str] = "TWINE_USERNAME",
        twine_password_env_var: Optional[str] = "TWINE_PASSWORD",
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        Runs:

        ```
        pip3 install --upgrade twine
        python3 -m twine upload --non-interactive --disable-progress-bar dist/*
        ```

        * Requires artifacts from a build job under `dist/` (e.g. from `bdist_wheel()`)

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `twine`
            * `job_opts.stage` defaults to `deploy`

        Args:
            twine_repository_url (str): The URL to the PyPI repository the python artifacts will be deployed to. Defaults
                to `None`, which means the package is published to `https://pypi.org`.
            twine_username_env_var (Optional[str]): The name of the environment variable, which contains the username value.
                **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue! Defaults to `TWINE_USERNAME`.
            twine_password_env_var (Optional[str]): The name of the environment variable, which contains the password.
                **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue! Defaults to `TWINE_PASSWORD`.
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "twine"
        if not job_opts.stage:
            job_opts.stage = "deploy"

        job_opts.script = [
            "pip3 install --upgrade twine",
            "python3 -m twine upload --non-interactive --disable-progress-bar dist/*",
        ]

        super().__init__(**job_opts.__dict__)

        self.add_variables(
            TWINE_USERNAME=f"${twine_username_env_var}",
            TWINE_PASSWORD=f"${twine_password_env_var}",
        )

        if twine_repository_url:
            self.add_variables(TWINE_REPOSITORY_URL=twine_repository_url)
