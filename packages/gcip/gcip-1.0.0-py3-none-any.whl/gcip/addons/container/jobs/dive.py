__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Daniel von Eßen"
__email__ = "daniel.von-essen@deutschebahn.com"

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


def _is_float_between_zero_and_one(validate: float) -> bool:
    """
    Helper function to validate given arguments type and range.

    If `validate` is not of type float or not between 0.0 and 1.0 function returns `False`.
            Otherwise function returns `True`
    Args:
        validate (float): Argument to validate.

    Returns:
        bool:
    """

    if not isinstance(validate, float):
        raise TypeError("Argument is not of type float.")
    if not 0 <= validate <= 1:
        raise ValueError("Argument is not between 0.0 and 1.0.")
    return True


@dataclass
class ScanOpts:
    image_path: Optional[str] = None
    image_name: Optional[str] = None
    highest_user_wasted_percent: Optional[float] = None
    highest_wasted_bytes: Optional[float] = None
    lowest_efficiency: Optional[float] = None
    ignore_errors: bool = False
    source: str = "docker-archive"
    job_opts: Optional[JobOpts] = None


class Scan(Job):
    def __init__(
        self,
        *,
        image_path: Optional[str] = None,
        image_name: Optional[str] = None,
        highest_user_wasted_percent: Optional[float] = None,
        highest_wasted_bytes: Optional[float] = None,
        lowest_efficiency: Optional[float] = None,
        ignore_errors: bool = False,
        source: str = "docker-archive",
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        Scan your images with [wagoodman/dive](https://github.com/wagoodman/dive).

        `dive` will scan your container image layers and will output the efficency of each layer.
        You can see which layer and which file is consuming the most storage and optimize the layers if possible.
        It prevents container images and its layers beeing polluted with files like apt or yum cache's.
        The output produced by `dive` is uploaded as an artifact to the GitLab instance.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `dive`
            * `job_opts.stage` defaults to `check`
            * `job_opts.image` defaults to `PredefinedImages.DIVE`. The image must contain the `dive` binary.

        Args:
            image_path (Optional[str]): Path to the image can be either a remote container registry,
                as well as a local path to an image. Defaults to `PredefinedVariables.CI_PROJECT_PATH`.
            image_name (Optional[str]): Name of the container image to scan, if `source` is `docker-archive` argument gets prefix `.tar`.
                Defaults to PredefinedVariables.CI_PROJECT_NAME.
            highest_user_wasted_percent (Optional[float]): Highest allowable percentage of bytes wasted
                (as a ratio between 0-1), otherwise CI validation will fail. (default "0.1"). Defaults to None.
            highest_wasted_bytes (Optional[float]): Highest allowable bytes wasted, otherwise CI validation will fail.
                (default "disabled"). Defaults to None.
            lowest_efficiency (Optional[float]): Lowest allowable image efficiency (as a ratio between 0-1),
                otherwise CI validation will fail. (default "0.9"). Defaults to None.
            ignore_errors (Optional[bool]): Ignore image parsing errors and run the analysis anyway. Defaults to False.
            source (Optional[str]): The container engine to fetch the image from. Allowed values: docker, podman, docker-archive
                (default "docker"). Defaults to "docker-archive".
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "dive"
        if not job_opts.stage:
            job_opts.stage = "check"
        if not job_opts.image:
            job_opts.image = PredefinedImages.DIVE

        if not image_path:
            image_path = "/" + PredefinedVariables.CI_PROJECT_PATH
        if image_path and image_path.endswith("/"):
            image_path = image_path[:-1]

        if not image_name:
            image_name = PredefinedVariables.CI_PROJECT_NAME

        if source == "docker-archive":
            image_name = f"{image_name}.tar".replace("/", "_")

        dive_command = ["dive", f"{source}://{image_path}/{image_name}", "--ci"]

        if highest_user_wasted_percent and _is_float_between_zero_and_one(highest_user_wasted_percent):
            dive_command.append(f'--highestUserWastedPercent "{highest_user_wasted_percent}"')
        if highest_wasted_bytes and _is_float_between_zero_and_one(highest_wasted_bytes):
            dive_command.append(f'--highestWastedBytes "{highest_wasted_bytes}"')
        if lowest_efficiency and _is_float_between_zero_and_one(lowest_efficiency):
            dive_command.append(f'--lowestEfficiency "{lowest_efficiency}"')
        if ignore_errors:
            dive_command.append("--ignore-errors")

        dive_command.append("|tee " + path.join(PredefinedVariables.CI_PROJECT_DIR, "dive.txt"))

        job_opts.script = [
            "set -eo pipefail",
            " ".join(dive_command),
        ]

        super().__init__(**job_opts.__dict__)

        self.artifacts.add_paths("dive.txt")
