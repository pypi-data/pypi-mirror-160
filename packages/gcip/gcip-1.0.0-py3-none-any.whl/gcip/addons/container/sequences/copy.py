from typing import Union, Optional
from warnings import warn
from dataclasses import dataclass

from gcip.core.cache import Cache, CacheKey
from gcip.core.sequence import Sequence
from gcip.core.variables import PredefinedVariables
from gcip.addons.container.jobs import dive, crane, trivy
from gcip.addons.container.registries import Registry
from gcip.addons.container.sequences.helper import (
    add_dive_scan_job_to_sequence,
    add_crane_push_job_to_sequence,
    add_trivy_scan_job_to_sequence,
    add_trivy_ignore_file_check_to_sequence,
)


@dataclass
class CopyContainerOpts:
    image_name: str
    image_tag: str
    dst_registry: Union[Registry, str] = Registry.DOCKER
    src_registry: Union[Registry, str] = Registry.DOCKER
    do_dive_scan: bool = True
    do_trivy_scan: bool = True
    do_trivy_ignore_file_check: bool = True
    crane_pull_opts: Optional[crane.PullOpts] = None
    dive_scan_opts: Optional[dive.ScanOpts] = None
    trivy_scan_opts: Optional[trivy.ScanLocalImageOpts] = None
    trivy_ignore_file_check_opts: Optional[trivy.TrivyIgnoreFileCheckOpts] = None
    crane_push_opts: Optional[crane.PushOpts] = None


class CopyContainer(Sequence):
    def __init__(
        self,
        *,
        image_name: str,
        image_tag: str,
        dst_registry: Union[Registry, str] = Registry.DOCKER,
        src_registry: Union[Registry, str] = Registry.DOCKER,
        do_dive_scan: bool = True,
        do_trivy_scan: bool = True,
        do_trivy_ignore_file_check: bool = True,
        crane_pull_opts: Optional[crane.PullOpts] = None,
        dive_scan_opts: Optional[dive.ScanOpts] = None,
        trivy_scan_opts: Optional[trivy.ScanLocalImageOpts] = None,
        trivy_ignore_file_check_opts: Optional[trivy.TrivyIgnoreFileCheckOpts] = None,
        crane_push_opts: Optional[crane.PushOpts] = None,
    ) -> None:
        """
        Creates a `gcip.Sequence` to pull, scan and push a container image.

        The pull step is executed by `gcip.addons.container.jobs.crane.pull`, it will pull the container image an outputs it to a tarball.
        There are two scan's, optimization scan with `gcip.addons.container.jobs.dive.scan_local_image` to scan storage wasting in container image
        and a vulnerability scan with `gcip.addons.container.jobs.trivy.scan`. Both outputs are uploaded as an artifact to the GitLab instance.
        Built container image is uploaded with `gcip.addons.container.jobs.crane.push`.

        Args:
            src_registry (Union[Registry, str], optional): Container registry to pull the image from. If the container registry needs authentication,
                you have to provide a `gcip.addons.container.config.DockerClientConfig` object with credentials. Defaults to Registry.DOCKER.
            dst_registry (Union[Registry, str]): Container registry to push the image to. If the container registry needs authentication,
                you have to provide a `gcip.addons.container.config.DockerClientConfig` object with credentials. Defaults to Registry.DOCKER.
            image_name (str): Image name with stage in the registry. e.g. username/image_name.
            image_tag (str): Container image tag to pull from `src_registry` and push to `dst_registry`.
            do_dive_scan (Optional[bool]): Set to `False` to skip the Dive scan job. Defaults to True.
            do_trivy_scan (Optional[bool]): Set to `False` to skip the Trivy scan job. Defaults to True.
            do_trivyignore_check (Optional[bool]): Set to `False` to skip the existance check of the `.trivyignore` file. Defaults to True.

        Returns:
            Sequence: `gcip.Sequence` to pull, scan and push a container image.
        """
        super().__init__()

        """
        We decided to use caches instead of artifacts to pass the Docker image tar archive from one job to another.
        This is because those tar archives could become very large - especially larger then the maximum artifact size limit.
        This limit can just be adjusted by the admin of the gitlab instance, so your pipeline would never work, your Gitlab
        provider would not adjust this limit for you. For caches on the other hand you can define storage backends at the
        base of your Gitlab runners.

        Furthermore we set the cache key to the pipeline ID. This is because the name and tag of the image does not ensure that
        the downloaded tar is unique, as the image behind the image tag could be overridden. So we ensure uniqueness by downloading
        the image once per pipeline.
        """

        self.cache = Cache(paths=["image"], cache_key=CacheKey(PredefinedVariables.CI_PIPELINE_ID + image_name + image_tag))

        #
        # crane pull
        #
        if crane_pull_opts:
            if crane_pull_opts.src_registry:
                warn("crane_pull_opts.src_registry will be overridden by CopyContainer.src_registry")
            if crane_pull_opts.image_name:
                warn("crane_pull_opts.image_name will be overridden by CopyContainer.image_name")

            crane_pull_opts.src_registry = src_registry
            crane_pull_opts.image_name = image_name
        else:
            crane_pull_opts = crane.PullOpts(src_registry=src_registry, image_name=image_name)

        crane_pull_opts = crane_pull_opts

        if crane_pull_opts.image_tag:
            warn("crane_pull_opts.image_tag will be overridden by CopyContainer.image_tag")
        if crane_pull_opts.tar_path:
            warn("crane_pull_opts.tar_path will be overridden by CopyContainer's internal cache path")
        if crane_pull_opts.job_opts and crane_pull_opts.job_opts.cache:
            warn("crane_pull_opts.job_opts.cache will be overridden by CopyContainer's cache")

        crane_pull_opts.image_tag = image_tag
        crane_pull_opts.tar_path = self.cache.paths[0]

        self.crane_pull_job = crane.Pull(**crane_pull_opts.__dict__)
        self.crane_pull_job.set_cache(self.cache)
        self.add_children(self.crane_pull_job)

        #
        # dive scan
        #

        if do_dive_scan:
            self.dive_scan_job = add_dive_scan_job_to_sequence(
                sequence=self,
                dive_scan_opts=dive_scan_opts,
                sequence_cache=self.cache,
                image_name=image_name,
            )
            self.dive_scan_job.add_needs(self.crane_pull_job)

        #
        # trivy scan
        #

        if do_trivy_scan:
            self.trivy_scan_job = add_trivy_scan_job_to_sequence(
                sequence=self,
                trivy_scan_opts=trivy_scan_opts,
                sequence_cache=self.cache,
                image_name=image_name,
            )
            self.trivy_scan_job.add_needs(self.crane_pull_job)

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

        self.crane_push_job = add_crane_push_job_to_sequence(
            sequence=self,
            crane_push_opts=crane_push_opts,
            sequence_cache=self.cache,
            image_name=image_name,
            image_tag=image_tag,
            registry=dst_registry,
        )

        self.crane_push_job.add_needs(self.crane_pull_job)
        if do_dive_scan:
            self.crane_push_job.add_needs(self.dive_scan_job)
        if do_trivy_scan:
            self.crane_push_job.add_needs(self.trivy_scan_job)
