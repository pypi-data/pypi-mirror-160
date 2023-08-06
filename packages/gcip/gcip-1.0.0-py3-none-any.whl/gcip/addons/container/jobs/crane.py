import os
from typing import Union, Optional
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


@dataclass
class CopyOpts:
    src_registry: Union[Registry, str]
    dst_registry: Union[Registry, str]
    job_opts: Optional[JobOpts] = None
    docker_client_config: Optional[DockerClientConfig] = None


class Copy(Job):
    def __init__(
        self,
        *,
        src_registry: Union[Registry, str],
        dst_registry: Union[Registry, str],
        docker_client_config: Optional[DockerClientConfig] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """
        Creates a job to copy container images with `crane`.
        See [`crane`](https://github.com/google/go-containerregistry/tree/main/cmd/crane)

        Copying an image is usfull, if you want to have container images as close as possible
        to your cluster or servers.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `crane-copy`
            * `job_opts.stage` defaults to `deploy`
            * `job_opts.image` defaults to `PredefinedImages.CRANE`. This is the Gitlab executor image this job should run with. It must
              contain the `crane` binary.

        Args:
            src_registry (str): Registry URL to copy container image from.
            dst_registry (str): Registry URL to copy container image to.
            docker_client_config (Optional[DockerClientConfig], optional): Creates the Docker configuration file base on objects settings,
                used by crane to authenticate against given registries. Defaults to None.
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "crane-copy"
        if not job_opts.stage:
            job_opts.stage = "deploy"
        if not job_opts.image:
            job_opts.image = PredefinedImages.CRANE

        if docker_client_config:
            job_opts.script = docker_client_config.get_shell_command()
        else:
            job_opts.script = []

        job_opts.script.extend(
            [
                f"crane validate --remote {src_registry}",
                f"crane copy {src_registry} {dst_registry}",
            ]
        )

        super().__init__(**job_opts.__dict__)


@dataclass
class PushOpts:
    dst_registry: Optional[Union[Registry, str]] = None
    job_opts: Optional[JobOpts] = None
    tar_path: Optional[str] = None
    image_name: Optional[str] = None
    image_tag: Optional[str] = None
    docker_client_config: Optional[DockerClientConfig] = None


@dataclass
class Push(Job):
    def __init__(
        self,
        *,
        dst_registry: Optional[Union[Registry, str]] = None,
        job_opts: Optional[JobOpts] = None,
        tar_path: Optional[str] = None,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        docker_client_config: Optional[DockerClientConfig] = None,
    ) -> None:
        """
        Creates a job to push container image to remote container registry with `crane`.

        The image to copy must be in a `tarball` format. It gets validated with crane
        and is pushed to `dst_registry` destination registry.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `crane-push`
            * `job_opts.stage` defaults to `deploy`
            * `job_opts.image` defaults to `PredefinedImages.CRANE`. This is the Gitlab executor image this job should run with. It must
              contain the `crane` binary.

        Args:
            dst_registry (str): Registry URL to copy container image to.
            tar_path (Optional[str], optional): Path where to find the container image tarball.
                If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_DIR`. Defaults to None.
            image_name (Optional[str], optional): Container image name, searched for in `image_path` and gets `.tar` appended.
                If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_NAME`. Defaults to None.
            image_tag (Optional[str]): The tag the image will be tagged with.
                Defaults to `PredefinedVariables.CI_COMMIT_REF_NAME` or `PredefinedVariables.CI_COMMIT_TAG`.
            docker_client_config (Optional[DockerClientConfig], optional): Creates the Docker configuration file base on objects settings,
                to authenticate against given registries. Defaults to a `DockerClientConfig` with login to the official Docker Hub
                and expecting credentials given as environment variables `REGISTRY_USER` and `REGISTRY_LOGIN`.
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "crane-push"
        if not job_opts.stage:
            job_opts.stage = "deploy"
        if not job_opts.image:
            job_opts.image = PredefinedImages.CRANE

        if not tar_path:
            tar_path = PredefinedVariables.CI_PROJECT_DIR
        if not image_name:
            image_name = PredefinedVariables.CI_PROJECT_NAME
        image_path = image_name.replace("/", "_")

        if not image_tag:
            if PredefinedVariables.CI_COMMIT_TAG:
                image_tag = PredefinedVariables.CI_COMMIT_TAG
            else:
                image_tag = PredefinedVariables.CI_COMMIT_REF_NAME

        if not docker_client_config:
            docker_client_config = DockerClientConfig().add_auth(registry=Registry.DOCKER)
        job_opts.script = docker_client_config.get_shell_command()

        job_opts.script.extend(
            [
                f"crane validate --tarball {tar_path}/{image_path}.tar",
                f"crane push {tar_path}/{image_path}.tar {dst_registry}/{image_name}:{image_tag}",
            ]
        )

        if image_tag in ["main", "master"]:
            job_opts.script.append(f"crane push {tar_path}/{image_path}.tar {dst_registry}/{image_name}:latest")

        super().__init__(**job_opts.__dict__)


@dataclass
class PullOpts:
    src_registry: Optional[Union[Registry, str]] = None
    image_name: Optional[str] = None
    image_tag: Optional[str] = None
    tar_path: Optional[str] = None
    docker_client_config: Optional[DockerClientConfig] = None
    job_opts: Optional[JobOpts] = None


class Pull(Job):
    def __init__(
        self,
        *,
        src_registry: Optional[Union[Registry, str]] = None,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        tar_path: Optional[str] = None,
        docker_client_config: Optional[DockerClientConfig] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:

        """
        Creates a job to pull container image from remote container registry with `crane`.

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `crane`
            * `job_opts.stage` defaults to `pull`
            * `job_opts.image` defaults to `PredefinedImages.CRANE`. This is the Gitlab executor image this job should run with. It must
              contain the `crane` binary.

        Args:
            src_registry (str): Registry URL to pull container image from.
            image_name (str): Container image with namespace to pull from `src_registry`.
                If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_NAME`. Defaults to None.
            image_tag (str): Tag of the image which will be pulled. Defaults to "latest".
            tar_path (Optional[str], optional): Path where to save the container image tarball.
                If `None` it defaults internally to `PredefinedVariables.CI_PROJECT_DIR`. Defaults to None.
            docker_client_config (Optional[DockerClientConfig], optional): Creates the Docker configuration file base on objects settings,
                to authenticate against given registries. Defaults to a `DockerClientConfig` with login to the official Docker Hub
                and expecting credentials given as environment variables `REGISTRY_USER` and `REGISTRY_LOGIN`.
        """
        if not job_opts:
            job_opts = JobOpts()

        job_opts = job_opts

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "crane"
        if not job_opts.stage:
            job_opts.stage = "pull"
        if not job_opts.image:
            job_opts.image = PredefinedImages.CRANE

        if not image_name:
            image_name = PredefinedVariables.CI_PROJECT_NAME
        if not image_tag:
            image_tag = "latest"
        if not tar_path:
            tar_path = PredefinedVariables.CI_PROJECT_DIR

        image_path = image_name.replace("/", "_")

        if not docker_client_config:
            docker_client_config = DockerClientConfig().add_auth(registry=Registry.DOCKER)
        job_opts.script = docker_client_config.get_shell_command()

        job_opts.script.extend(
            [
                f"mkdir -p {os.path.normpath(tar_path)}",
                f"crane pull {src_registry}/{image_name}:{image_tag} {tar_path}/{image_path}.tar",
            ]
        )

        super().__init__(**job_opts.__dict__)
