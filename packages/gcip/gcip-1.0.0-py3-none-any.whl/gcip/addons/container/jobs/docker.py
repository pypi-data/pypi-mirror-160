"""This modules provide Jobs executing [Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/) scripts

Those require [Docker to be installed](https://docs.docker.com/engine/install/) on the Gitlab runner.
"""

from typing import Optional
from dataclasses import dataclass

from gcip.core.job import (
    Job,
    JobOpts,
    ScriptArgumentNotAllowedError,
)

__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"


@dataclass
class BuildOpts:
    repository: str
    tag: Optional[str] = None
    context: str = "."
    job_opts: Optional[JobOpts] = None


class Build(Job):
    def __init__(
        self,
        *,
        repository: str,
        tag: Optional[str] = None,
        context: str = ".",
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """Runs [```docker build```](https://docs.docker.com/engine/reference/commandline/build/)

        Example:

        ```
        from gcip.addons.container.job.docker import Build
        build_job = Build(BuildOpts(repository="myrepo/myimage", tag="v0.1.0"))
        ```

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `docker`
            * `job_opts.stage` defaults to `build`

        Args:
            repository (str): The Docker repository name ```([<registry>/]<image>)```.
            tag (Optional[str]): A Docker image tag applied to the image. Defaults to `None` which no tag is provided
                to the docker build command. Docker should then apply the default tag ```latest```.
            context (str): The Docker build context (the directory containing the Dockerfile). Defaults to
                the current directory `.`.
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "docker"
        if not job_opts.stage:
            job_opts.stage = "build"

        fq_image_name = repository
        if tag:
            fq_image_name += f":{tag}"

        job_opts.script = f"docker build -t {fq_image_name} {context}"

        super().__init__(**job_opts.__dict__)
        self.add_variables(DOCKER_DRIVER="overlay2", DOCKER_TLS_CERTDIR="")


@dataclass
class PushOpts:
    container_image: str
    registry: Optional[str] = None
    tag: Optional[str] = None
    user_env_var: Optional[str] = None
    login_env_var: Optional[str] = None
    job_opts: Optional[JobOpts] = None


class Push(Job):
    def __init__(
        self,
        *,
        container_image: str,
        registry: Optional[str] = None,
        tag: Optional[str] = None,
        user_env_var: Optional[str] = None,
        login_env_var: Optional[str] = None,
        job_opts: Optional[JobOpts] = None,
    ) -> None:
        """Runs [```docker push```](https://docs.docker.com/engine/reference/commandline/push/)
        and optionally [```docker login```](https://docs.docker.com/engine/reference/commandline/login/) before.

        Example:

        ```python
        from gcip.addons.container.docker import Push
        push_job = Push(PushOpts(
                        registry="docker.pkg.github.com/dbsystel/gitlab-ci-python-library",
                        image="gcip",
                        tag="v0.1.0",
                        user_env_var="DOCKER_USER",
                        login_env_var="DOCKER_TOKEN"
                    ))
        ```

        The `user_env_var` and `login_env_var` should be created as *protected* and *masked*
        [custom environment variable configured
        in the UI](https://git.tech.rz.db.de/help/ci/variables/README#create-a-custom-variable-in-the-ui).

        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `docker`
            * `job_opts.stage` defaults to `deploy`

        Args:
            registry (Optional[str]): The Docker registry the image should be pushed to.
                Defaults to `None` which targets to the official Docker Registry at hub.docker.com.
            image (str): The name of the Docker image to push to the `registry`.
            tag (Optional[str]): The Docker image tag that should be pushed to the `registry`. Defaults to ```latest```.
            user_env_var (Optional[str]): If you have to login to the registry before the push, you have to provide
                the name of the environment variable, which contains the username value, here.
                **DO NOT PROVIDE THE USERNAME VALUE ITSELF!** This would be a security issue!
                Defaults to `None` which skips the docker login attempt.
            login_env_var (Optional[str]): If you have to login to the registry before the push, you have to provide
                the name of the environment variable, which contains the password or token, here.
                **DO NOT PROVIDE THE LOGIN VALUE ITSELF!** This would be a security issue!
                Defaults to `None` which skips the docker login attempt.
        """
        if not job_opts:
            job_opts = JobOpts()

        if job_opts.script:
            raise ScriptArgumentNotAllowedError()
        if not job_opts.name:
            job_opts.name = "docker"
        if not job_opts.stage:
            job_opts.stage = "deploy"

        job_opts.script = []
        if user_env_var and login_env_var:
            job_opts.script.append(f'docker login -u "${user_env_var}" -p "${login_env_var}"')

        fq_image_name = container_image
        if registry:
            fq_image_name = f"{registry}/{fq_image_name}"
        if tag:
            fq_image_name += f":{tag}"

        job_opts.script.append(f"docker push {fq_image_name}")

        super().__init__(**job_opts.__dict__)
