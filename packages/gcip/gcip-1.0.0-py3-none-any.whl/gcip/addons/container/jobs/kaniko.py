import os
from typing import Dict, List, Union, Optional
from dataclasses import dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)
from gcip.core.variables import PredefinedVariables
from gcip.addons.container.config import DockerClientConfig
from gcip.addons.container.images import PredefinedImages
from gcip.addons.container.registries import Registry

__author__ = "Daniel von Eßen"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Daniel von Eßen", "Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


@dataclass
class ExecuteOpts:
    job_opts: Optional[JobOpts] = None
    context: Optional[str] = None
    image_name: Optional[str] = None
    image_tag: Optional[str] = None
    registries: Optional[List[Union[Registry, str]]] = None
    tar_path: Optional[str] = None
    build_args: Optional[Dict[str, str]] = None
    build_target: Optional[str] = None
    dockerfile: Optional[str] = None
    enable_push: bool = False
    docker_client_config: Optional[DockerClientConfig] = None
    verbosity: Optional[str] = None


class Execute(Job):
    def __init__(
        self,
        *,
        context: Optional[str] = None,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        registries: Optional[List[Union[Registry, str]]] = None,
        tar_path: Optional[str] = None,
        build_args: Optional[Dict[str, str]] = None,
        build_target: Optional[str] = None,
        dockerfile: Optional[str] = None,
        enable_push: bool = False,
        docker_client_config: Optional[DockerClientConfig] = None,
        verbosity: Optional[str] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        Creates a job which builds container images.

        This job creates images depending on git branches.
        e.g If the branch which gets pushed to the remote is named `my_awsome_feature` the image will be tagged with `my-awsome-feature`.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `kaniko`
            * `job_opts.stage` defaults to `build`
            * `job_opts.image` defaults to `PredefinedImages.KANIKO`. This is the Gitlab executor image this job should run with. It must
              contain the kaniko executor binary.

        Args:
            context (Optional[str], optional): Context which will be send to kaniko. Defaults to `None` which implies the local
                directory is the context.
            image_name (Optional[str], optional): Image name which will be created. Defaults to PredefinedVariables.CI_PROJECT_NAME.
            image_tag (Optional[str]): The tag the image will be tagged with.
                Defaults to `PredefinedVariables.CI_COMMIT_REF_NAME` or `PredefinedVariables.CI_COMMIT_TAG`.
            registries (Optional[List[str]], optional): List of container registries to push created image to. Defaults to an empty list.
            tar_path (Optional[str], optional): Container images created by kaniko are tarball files.
                This is the path where to store the image, will be named with suffix `.tar`. This path will be created if not present.
                Defaults to `None` which implies the image will be pushed to ```hub.docker.com```.
            build_args (Dict[str, str], optional): Container build arguments, used to instrument the container image build. Defaults to {}.
            build_target (Optional[str], optional): For container multistage builds name of the build stage you want to create.
                Image tag will be appended with the build_target. e.g. latest-buildtarget. Defaults to None.
            dockerfile (str, optional): Name of the dockerfile to use. File is relative to context. Defaults to "Dockerfile".
            enable_push (bool, optional): Enable push to container registry, disabled to allow subsequent jobs to act on container tarball.
                Defaults to False.
            docker_client_config (Optional[DockerClientConfig], optional): Creates the Docker configuration file base on objects settings,
                to authenticate against given registries. Defaults to a `DockerClientConfig` with login to the official Docker Hub
                and expecting credentials given as environment variables `REGISTRY_USER` and `REGISTRY_LOGIN`.
            verbosity (str, optional): Verbosity of kaniko logging. Defaults to "info".
        """
        if not job_opts:
            job_opts = JobOpts()

        job_opts = job_opts

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "kaniko"
        if not job_opts.stage:
            job_opts.stage = "build"
        if not job_opts.image:
            job_opts.image = PredefinedImages.KANIKO

        jobScripts: List[str] = []

        if not image_name:
            image_name = PredefinedVariables.CI_PROJECT_NAME

        if not image_tag:
            if PredefinedVariables.CI_COMMIT_TAG:
                image_tag = PredefinedVariables.CI_COMMIT_TAG
            elif PredefinedVariables.CI_COMMIT_REF_NAME:
                image_tag = PredefinedVariables.CI_COMMIT_REF_NAME

        image_tag_postfix = ""
        if image_tag:
            image_tag_postfix = f":{image_tag}"

        if not context:
            context = PredefinedVariables.CI_PROJECT_DIR
        else:
            context = os.path.normpath(context)

        if not dockerfile:
            dockerfile = f"{PredefinedVariables.CI_PROJECT_DIR}/Dockerfile"

        if not docker_client_config:
            docker_client_config = DockerClientConfig()
            docker_client_config.add_auth(registry=Registry.DOCKER)

        # Set static config path. Kaniko uses /kaniko/.docker/config.json path
        docker_client_config.set_config_file_path("/kaniko/.docker/config.json")
        jobScripts.extend(docker_client_config.get_shell_command())

        executor_cmd = ["executor"]
        executor_cmd.append(f"--context {context}")
        executor_cmd.append(f"--dockerfile {dockerfile}")

        if tar_path:
            jobScripts.append(f"mkdir -p {os.path.normpath(tar_path)}")
            image_path = image_name.replace("/", "_")
            executor_cmd.append(f"--tarPath {os.path.join(tar_path, image_path)}.tar")

        if verbosity:
            executor_cmd.append(f"--verbosity {verbosity}")

        # Disable push to registries.
        if not enable_push:
            executor_cmd.append("--no-push")

        # Check if multistage build is wanted.
        # Add --target flag to executor and prefix build_target "-"
        build_target_postfix = ""
        if build_target:
            executor_cmd.append(f"--target {build_target}")
            build_target_postfix = f"-{build_target}"

        # Compose build arguments.
        if build_args:
            for k, v in build_args.items():
                executor_cmd.append(f"--build-arg '{k}={v}'")

        # Extend executor command with --destination per registry
        if registries is None or len(registries) == 0:
            executor_cmd.append(f"--destination {image_name}{image_tag_postfix}{build_target_postfix}")
            if image_tag and (image_tag == "main" or image_tag == "master"):
                executor_cmd.append(f"--destination {image_name}:latest{build_target_postfix}")

        if registries:
            for registry in registries:
                executor_cmd.append(f"--destination {registry}/{image_name}{image_tag_postfix}{build_target_postfix}")
                if image_tag and (image_tag == "main" or image_tag == "master"):
                    executor_cmd.append(f"--destination {registry}/{image_name}:latest{build_target_postfix}")

        jobScripts.append(" ".join(executor_cmd))

        job_opts.script = jobScripts

        super().__init__(**job_opts.__dict__)
