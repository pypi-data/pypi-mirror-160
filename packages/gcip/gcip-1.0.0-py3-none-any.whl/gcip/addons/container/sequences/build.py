__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach", "Daniel von Eßen"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Daniel von Eßen"
__email__ = "daniel.von-essen@deutschebahn.com"

from typing import Union, Optional
from warnings import warn
from dataclasses import dataclass

from gcip.core.cache import Cache
from gcip.core.sequence import Sequence
from gcip.addons.container.jobs import (
    dive,
    crane,
    trivy,
    kaniko,
)
from gcip.addons.container.registries import Registry
from gcip.addons.container.sequences.helper import (
    add_dive_scan_job_to_sequence,
    add_crane_push_job_to_sequence,
    add_trivy_scan_job_to_sequence,
    add_trivy_ignore_file_check_to_sequence,
)


@dataclass
class FullContainerSequenceOpts:
    image_name: Optional[str] = None
    image_tag: Optional[str] = None
    registry: Union[Registry, str] = Registry.DOCKER
    do_dive_scan: bool = True
    do_trivy_scan: bool = True
    do_trivy_ignore_file_check: bool = True
    do_crane_push: bool = True
    kaniko_execute_opts: Optional[kaniko.ExecuteOpts] = None
    dive_scan_opts: Optional[dive.ScanOpts] = None
    trivy_scan_opts: Optional[trivy.ScanLocalImageOpts] = None
    trivy_ignore_file_check_opts: Optional[trivy.TrivyIgnoreFileCheckOpts] = None
    crane_push_opts: Optional[crane.PushOpts] = None


class FullContainerSequence(Sequence):
    def __init__(
        self,
        *,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        registry: Union[Registry, str] = Registry.DOCKER,
        do_dive_scan: bool = True,
        do_trivy_scan: bool = True,
        do_trivy_ignore_file_check: bool = True,
        do_crane_push: bool = True,
        kaniko_execute_opts: Optional[kaniko.ExecuteOpts] = None,
        dive_scan_opts: Optional[dive.ScanOpts] = None,
        trivy_scan_opts: Optional[trivy.ScanLocalImageOpts] = None,
        trivy_ignore_file_check_opts: Optional[trivy.TrivyIgnoreFileCheckOpts] = None,
        crane_push_opts: Optional[crane.PushOpts] = None,
    ) -> None:
        """
        Creates a `gcip.Sequence` to build, scan and push a container image.

        The build step is executed by `gcip.addons.container.jobs.kaniko.execute`, it will build the container image an outputs it to a tarball.
        There are two scan's, optimization scan with `gcip.addons.container.jobs.dive.scan_local_image` to scan storage wasting in container image
        and a vulnerability scan with `gcip.addons.container.jobs.trivy.scan`. Both outputs are uploaded as an artifact to the GitLab instance.
        The container image is uploaded with `gcip.addons.container.jobs.crane.push`.

        Args:
            registry (Union[Registry, str], optional): Container registry to push the image to. If the container registry needs authentication,
                you have to provide a `gcip.addons.container.config.DockerClientConfig` object with credentials. Defaults to Registry.DOCKER.
            image_name (Optional[str]): Image name with stage in the registry. e.g. username/image_name.
                Defaults to `gcip.core.variables.PredefinedVariables.CI_PROJECT_NAME`.
            image_tag (Optional[str]): Image tag. The default is either `PredefinedVariables.CI_COMMIT_TAG` or
                `PredefinedVariables.CI_COMMIT_REF_NAME` depending of building from a git tag or from a branch.
            docker_client_config (Optional[DockerClientConfig], optional): Creates the Docker configuration file base on objects settings,
                to authenticate against given registries. Defaults to a `DockerClientConfig` with login to the official Docker Hub
                and expecting credentials given as environment variables `REGISTRY_USER` and `REGISTRY_LOGIN`.
            do_dive_scan (Optional[bool]): Set to `False` to skip the Dive scan job. Defaults to True.
            do_trivy_scan (Optional[bool]): Set to `False` to skip the Trivy scan job. Defaults to True.
            do_trivyignore_check (Optional[bool]): Set to `False` to skip the existance check of the `.trivyignore` file. Defaults to True.
            do_crane_push (Optional[bool]): Set to `False` to skip the Crane push job. Defaults to True.
        """
        super().__init__()

        self.cache = Cache(paths=["image"])

        #
        # kaniko
        #

        if not kaniko_execute_opts:
            kaniko_execute_opts = kaniko.ExecuteOpts()
        kaniko_execute_opts = kaniko_execute_opts

        if kaniko_execute_opts.image_name:
            warn("kaniko_execute_opts.image_name will be overridden by FullContainerSequenceOpts.image_name")
        if kaniko_execute_opts.image_tag:
            warn("kaniko_execute_opts.image_tag will be overridden by FullContainerSequenceOpts.image_tag")
        if kaniko_execute_opts.registries:
            warn("kaniko_execute_opts.registries will be overridden by FullContainerSequenceOpts.registries")
        if kaniko_execute_opts.tar_path:
            warn("kaniko_execute_opts.tar_path will be overridden by FullContainerSequence's internal cache path")
        if kaniko_execute_opts.job_opts and kaniko_execute_opts.job_opts.cache:
            warn("kaniko_execute_opts.job_opts.cache will be overridden by FullContainerSequence's cache")

        kaniko_execute_opts.image_name = image_name
        kaniko_execute_opts.image_tag = image_tag
        kaniko_execute_opts.registries = [registry]
        kaniko_execute_opts.tar_path = self.cache.paths[0]

        self.kaniko_execute_job = kaniko.Execute(**kaniko_execute_opts.__dict__)
        self.kaniko_execute_job.set_cache(self.cache)
        self.add_children(self.kaniko_execute_job)

        #
        # dive
        #

        self.dive_scan_job = None
        if do_dive_scan:
            self.dive_scan_job = add_dive_scan_job_to_sequence(
                sequence=self,
                dive_scan_opts=dive_scan_opts,
                sequence_cache=self.cache,
                image_name=image_name,
            )

        #
        # trivy
        #

        self.trivy_scan_job = None
        if do_trivy_scan:
            self.trivy_scan_job = add_trivy_scan_job_to_sequence(
                sequence=self,
                trivy_scan_opts=trivy_scan_opts,
                sequence_cache=self.cache,
                image_name=image_name,
            )

        #
        # trivy ignore file check
        #

        self.trivy_ignore_file_check_job = None
        if do_trivy_ignore_file_check:
            self.trivy_ignore_file_check_job = add_trivy_ignore_file_check_to_sequence(
                sequence=self,
                trivy_ignore_file_check_opts=trivy_ignore_file_check_opts,
            )

        #
        # crane push
        #

        self.crane_push_job = None
        if do_crane_push:
            self.crane_push_job = add_crane_push_job_to_sequence(
                sequence=self,
                crane_push_opts=crane_push_opts,
                sequence_cache=self.cache,
                image_name=image_name,
                image_tag=image_tag,
                registry=registry,
            )
