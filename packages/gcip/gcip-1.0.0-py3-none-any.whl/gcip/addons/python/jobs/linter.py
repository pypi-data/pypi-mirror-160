from typing import Optional
from dataclasses import dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)


class Flake8(Job):
    def __init__(self, job_opts: Optional[JobOpts] = None) -> None:
        """
        Runs:

        ```
        pip3 install --upgrade flake8
        flake8
        ```

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `flake8`
            * `job_opts.stage` defaults to `lint`
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "flake8"
        if not job_opts.stage:
            job_opts.stage = "lint"

        job_opts.script = [
            "pip3 install --upgrade flake8",
            "flake8",
        ]

        super().__init__(**job_opts.__dict__)


@dataclass
class MypyOpts:
    package_dir: str
    mypy_version: Optional[str] = "0.812"
    mypy_options: Optional[str] = None
    job_opts: Optional[JobOpts] = None


class Mypy(Job):
    def __init__(
        self,
        *,
        package_dir: str,
        mypy_version: Optional[str] = "0.812",
        mypy_options: Optional[str] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        Install mypy if not already installed.
        Execute mypy for `package_dir`.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `mypy`
            * `job_opts.stage` defaults to `lint`

        Args:
            package_dir (str): Package directory to type check.
            mypy_version (str, optional): If `mypy` is not already installed this version will be installed. Defaults to "0.812".
            mypy_options (Optional[str], optional): Adds arguments to mypy execution. Defaults to None.
        Returns:
            Job: gcip.Job
        """
        if not job_opts:
            job_opts = JobOpts()

        job_opts = job_opts

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "mypy"
        if not job_opts.stage:
            job_opts.stage = "lint"

        script = [f'pip3 freeze | grep -q "^mypy==" || pip3 install mypy=={mypy_version}']

        if mypy_options:
            script.append(f"mypy {mypy_options} {package_dir}")
        else:
            script.append(f"mypy {package_dir}")

        job_opts.script = script

        super().__init__(**job_opts.__dict__)


class Isort(Job):
    def __init__(self, job_opts: Optional[JobOpts] = None) -> None:
        """
        Runs:

        ```
        pip3 install --upgrade isort
        isort --check .
        ```

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `isort`
            * `job_opts.stage` defaults to `lint`
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "isort"
        if not job_opts.stage:
            job_opts.stage = "lint"

        job_opts.script = [
            "pip3 install --upgrade isort",
            "isort --check .",
        ]

        super().__init__(**job_opts.__dict__)
