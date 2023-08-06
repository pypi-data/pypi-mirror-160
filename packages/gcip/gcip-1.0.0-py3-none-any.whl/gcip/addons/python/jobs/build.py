from typing import Optional

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)
from gcip.addons.python.scripts import (
    pip_install_requirements,
)
from gcip.addons.linux.scripts.package_manager import (
    install_packages,
)


class BdistWheel(Job):
    def __init__(self, job_opts: Optional[JobOpts] = None) -> None:
        """
        Runs `python3 setup.py bdist_wheel` and installs project requirements
        before (`scripts.pip_install_requirements()`)

        * Requires a `requirements.txt` in your project folder containing at least `setuptools`
        * Creates artifacts under the path `dist/`

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `bdist_wheel`
            * `job_opts.stage` defaults to `build`
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "bdist_wheel"
        if not job_opts.stage:
            job_opts.stage = "build"

        job_opts.script = [
            pip_install_requirements(),
            "pip list | grep setuptools-git-versioning && " + install_packages("git"),
            "python3 setup.py bdist_wheel",
        ]

        super().__init__(**job_opts.__dict__)
        self.artifacts.add_paths("dist/")
