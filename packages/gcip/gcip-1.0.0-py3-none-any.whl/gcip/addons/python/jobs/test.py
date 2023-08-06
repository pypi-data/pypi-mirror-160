from typing import Optional

from gcip.lib import rules
from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)
from gcip.addons.python.scripts import (
    pip_install_requirements,
)
from gcip.addons.container.images import PredefinedImages


class Pytest(Job):
    def __init__(self, job_opts: Optional[JobOpts] = None) -> None:
        """
        Runs `pytest` and installs project requirements before (`scripts.pip_install_requirements()`)

        * Requires a `requirements.txt` in your project folder containing at least `pytest`

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `pytest`
            * `job_opts.stage` defaults to `test`
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "pytest"
        if not job_opts.stage:
            job_opts.stage = "test"

        job_opts.script = [
            pip_install_requirements(),
            "pytest",
        ]

        super().__init__(**job_opts.__dict__)


class EvaluateGitTagPep440Conformity(Job):
    def __init__(self, job_opts: Optional[JobOpts] = None) -> None:
        """
        Checks if the current pipelines `$CI_COMMIT_TAG` validates to a valid Python package version according to
        https://www.python.org/dev/peps/pep-0440

        This job already contains a rule to only run when a `$CI_COMMIT_TAG` is present (`rules.only_tags()`).

        Runs `pytest` and installs project requirements before (`scripts.pip_install_requirements()`)

        * Requires a `requirements.txt` in your project folder containing at least `pytest`

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `tag-pep440-conformity`
            * `job_opts.stage` defaults to `test`
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "tag-pep440-conformity"
        if not job_opts.stage:
            job_opts.stage = "test"
        if not job_opts.image:
            job_opts.image = PredefinedImages.GCIP

        job_opts.script = "python3 -m gcip.tools.evaluate_git_tag_pep440_conformity"

        super().__init__(**job_opts.__dict__)
        self.append_rules(rules.on_tags())
