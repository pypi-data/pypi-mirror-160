from os import path
from typing import Optional
from dataclasses import dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)
from gcip.core.variables import PredefinedVariables
from gcip.addons.container.images import PredefinedImages


@dataclass
class ScanLocalImageOpts:
    image_path: Optional[str] = None
    image_name: Optional[str] = None
    output_format: Optional[str] = None
    severity: Optional[str] = None
    vulnerability_types: Optional[str] = None
    exit_if_vulnerable: bool = True
    trivy_config: Optional[str] = None
    job_opts: Optional[JobOpts] = None


class ScanLocalImage(Job):
    def __init__(
        self,
        *,
        image_path: Optional[str] = None,
        image_name: Optional[str] = None,
        output_format: Optional[str] = None,
        severity: Optional[str] = None,
        vulnerability_types: Optional[str] = None,
        exit_if_vulnerable: bool = True,
        trivy_config: Optional[str] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """This job scanns container images to find vulnerabilities.

        This job fails with exit code 1 if severities are found.
        The scan output is printed to stdout and uploaded to the artifacts of GitLab.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `trivy`
            * `job_opts.stage` defaults to `check`
            * `job_opts.image` defaults to `PredefinedImages.TRIVY`. This is the Gitlab executor image this job should run with. It must
              contain the trivy binary.

        Args:
            image_path (Optional[str]): Path where to find the container image.
                If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_DIR`. Defaults to None.
            image_name (Optional[str]): Container image name, searched for in `image_path` and gets `.tar` appended.
                If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_NAME`. Defaults to None.
            output_format (Optional[str]): Scan output format, possible values (table, json). Internal default `table`.
                Defaults to None.
            severity (Optional[str]): Severities of vulnerabilities to be displayed (comma separated).
                Defaults internally to "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL". Defaults to None.
            vulnerability_types (Optional[str]): List of vulnerability types (comma separated).
                Defaults internally to "os,library". Defaults to None.
            exit_if_vulnerable (bool): Exit code when vulnerabilities were found. If true exit code is 1 else 0. Defaults to True.
            trivy_config (Optional[str]): Additional options to pass to `trivy` binary. Defaults to None.

            Raises:
            ScriptArgumentNotAllowedError: It is not allowed to use the `script` argument in **kwargs,
                `script` is already initialized.
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "trivy"
        if not job_opts.stage:
            job_opts.stage = "check"
        if not job_opts.image:
            job_opts.image = PredefinedImages.TRIVY

        if not image_path:
            image_path = PredefinedVariables.CI_PROJECT_DIR
        if not image_name:
            image_name = PredefinedVariables.CI_PROJECT_NAME
        image_name = image_name.replace("/", "_")

        trivy_cmd = ["trivy image"]
        trivy_cmd.append(f"--input {image_path}/{image_name}.tar")
        trivy_cmd.append("--no-progress")

        if output_format:
            trivy_cmd.append(f"--format {output_format}")

        if severity:
            trivy_cmd.append(f"--severity {severity}")

        if vulnerability_types:
            trivy_cmd.append(f"--vuln-type {vulnerability_types}")

        if exit_if_vulnerable:
            trivy_cmd.append("--exit-code 1")

        if trivy_config:
            trivy_cmd.append(trivy_config)

        trivy_cmd.append("|tee " + path.join(PredefinedVariables.CI_PROJECT_DIR, "trivi.txt"))

        job_opts.script = [
            "set -eo pipefail",
            " ".join(trivy_cmd),
            "trivy --version",
        ]

        super().__init__(**job_opts.__dict__)

        self.artifacts.add_paths("trivi.txt")


@dataclass
class TrivyIgnoreFileCheckOpts:
    trivyignore_path: Optional[str] = None
    job_opts: Optional[JobOpts] = None


class TrivyIgnoreFileCheck(Job):
    def __init__(
        self,
        *,
        trivyignore_path: Optional[str] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        This job checks if a .trivyignore file exists and is not empty and fails if so.

        If a .trivyignore file is found and not empty, by default the job fails with `exit 1`,
        the job is configured to allow failures so that the pipeline keeps running.
        This ensures the visibility of acknowledged CVE's in the .trivyignore file inside the pipline.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `trivyignore`
            * `job_opts.stage` defaults to `check`
            * `job_opts.image` defaults to `PredefinedImages.BUSYBOX`. This is the Gitlab executor image this job should run with. It must
              contain the `statd` binary.

        Args:
            trivyignore_path (Optional[str], optional): Path to the `.trivyignore` file. Defaults to `$CI_PROJECT_DIR/.trivyignore`.

        Raises:
            ScriptArgumentNotAllowedError: It is not allowed to use the `script` argument in **kwargs,
                `script` is already initialized.
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "trivyignore"
        if not job_opts.stage:
            job_opts.stage = "check"
        if not job_opts.image:
            job_opts.image = PredefinedImages.BUSYBOX
        if not job_opts.allow_failure:
            job_opts.allow_failure = 1
        if not trivyignore_path:
            trivyignore_path = f"{PredefinedVariables.CI_PROJECT_DIR}/.trivyignore"

        job_opts.script = [
            "set -eo pipefail",
            f'test -f {trivyignore_path} || {{ echo "{trivyignore_path} does not exists."; exit 0; }}',
            # The grep-regex (-E) will check for everything but (-v) empty lines ('^ *$') and comments (first character is '#')
            f"grep -vE '^ *(#.*)?$' {trivyignore_path} || {{ echo '{trivyignore_path} found but empty.'; exit 0; }}",
            f'echo "{trivyignore_path} not empty. Please check your vulnerabilities!"; exit 1;',
        ]

        super().__init__(**job_opts.__dict__)
