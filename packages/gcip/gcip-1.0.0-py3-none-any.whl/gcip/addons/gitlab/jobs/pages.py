import os
from typing import Optional
from dataclasses import dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)
from gcip.core.variables import PredefinedVariables
from gcip.addons.python.scripts import (
    pip_install_requirements,
)


def _gitlab_pages_path(subpath: str) -> str:
    """
    Ensures `subpath` is a subpath under `./public`.

    Args:
        subpath (str): Any path string is allowed, with or without leading slash.

    Returns:
        str: The path string `public/<subpath>`
    """
    if subpath != "":
        subpath = os.path.normpath(subpath)

        if os.path.isabs(subpath):
            subpath = subpath[1:]

    return os.path.join("public", subpath)


@dataclass
class AsciiDoctorOpts:
    source: str
    out_file: str
    job_opts: Optional[JobOpts] = None


class AsciiDoctor(Job):
    def __init__(
        self,
        *,
        source: str,
        out_file: str,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        Translate the AsciiDoc source FILE as Gitlab Pages HTML5 file.

        Runs `asciidoctor {source} -o public{out_file}`and stores the output
        as artifact under the `public` directory.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `asciidoctor-pages`
            * `job_opts.stage` defaults to `build`
            * `job_opts.image` defaults to `ruby:3-alpine`. This is the Gitlab executor image this job should run with. It must
              contain the `ruby` binary.

        Args:
            source (str): Source .adoc files to translate to HTML files.
            out_file (str): Output HTML file.
        """
        if not job_opts:
            job_opts = JobOpts()

        job_opts = job_opts

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "asciidoctor-pages"
        if not job_opts.stage:
            job_opts.stage = "build"
        if not job_opts.image:
            job_opts.image = "ruby:3-alpine"

        job_opts.script = [
            "gem install asciidoctor",
            f"asciidoctor {source} -o {_gitlab_pages_path(out_file)}",
        ]

        super().__init__(**job_opts.__dict__)
        self.artifacts.add_paths("public")


class Sphinx(Job):
    def __init__(self, job_opts: Optional[JobOpts] = None) -> None:
        """
        Runs `sphinx-build -b html -E -a docs public/${CI_COMMIT_REF_NAME}` and installs project requirements
        before (`pip_install_requirements()`)

        * Requires a `docs/requirements.txt` in your project folder` containing at least `sphinx`
        * Creates it artifacts for Gitlab Pages under `pages`

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `asciidoctor-pages`
            * `job_opts.stage` defaults to `build`
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "sphinx-pages"
        if not job_opts.stage:
            job_opts.stage = "build"

        job_opts.script = [
            pip_install_requirements("docs/requirements.txt"),
            f"sphinx-build -b html -E -a docs {_gitlab_pages_path(PredefinedVariables.CI_COMMIT_REF_SLUG)}",
        ]

        super().__init__(**job_opts.__dict__)
        self.artifacts.add_paths("public")


@dataclass
class Pdoc3Opts:
    module: str
    output_path: str = ""
    job_opts: Optional[JobOpts] = None


class Pdoc3(Job):
    def __init__(
        self,
        *,
        module: str,
        output_path: str = "",
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """Generate a HTML API documentation of you python code as Gitlab Pages.

        Runs `pdoc3 --html -f --skip-errors --output-dir public{path} {module}` and stores the output
        as artifact under the `public` directory.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `pdoc3-pages`
            * `job_opts.stage` defaults to `build`

        Args:
            module (str): The Python module name. This may be an import path resolvable in the current environment,
                or a file path to a Python module or package.
            output_path (str, optional): A sub path of the Gitlab Pages `public` directory to output generated HTML/markdown files to. Defaults to "/".

        Returns:
            Job: The Gitlab CI job generating Gitlab Pages with pdoc3.
        """
        if not job_opts:
            job_opts = JobOpts()

        job_opts = job_opts

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "pdoc3-pages"
        if not job_opts.stage:
            job_opts.stage = "build"

        job_opts.script = [
            "pip3 install pdoc3",
            f"pdoc3 --html -f --skip-errors --output-dir {_gitlab_pages_path(output_path)} {module}",
        ]

        super().__init__(**job_opts.__dict__)
        self.artifacts.add_paths("public")
