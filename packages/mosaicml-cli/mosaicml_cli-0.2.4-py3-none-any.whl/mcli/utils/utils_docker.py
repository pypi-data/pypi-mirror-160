"""Utils for accessing docker sdk"""
import logging
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Generator, List, Optional, Set

import docker

logger = logging.getLogger(__name__)


def get_docker_client() -> docker.APIClient:
    """Get the docker client
    """
    return docker.from_env(assert_hostname=True)


def get_image_tags(client: docker.APIClient) -> Set[str]:
    """Gets all unique image tags available
    """
    tags = set()
    for image in client.images.list():
        for tag in image.tags:
            tags.add(tag)
    return tags


def _get_common_path(path1: Path, path2: Path) -> Optional[Path]:
    """Returns a common path of two paths if there is one
    """
    while path1 is not None:
        try:
            path2.relative_to(path1)
            return path1
        except ValueError:
            path1 = path1.parent
    return None


@dataclass
class Dockerfile:
    """Abstracts components of a dockerfile to build
    """

    image: str
    args: Dict[str, str] = field(default_factory=dict)
    copy: List[str] = field(default_factory=list)
    path: Optional[str] = None

    def get_copy_command(self, directory: str) -> str:
        d = Path(directory).expanduser().absolute()

        path = Path(self.path or '.')
        long_path = path.expanduser().absolute()

        common = _get_common_path(long_path, d)
        if common is not None:
            docker_dir = path / d.relative_to(*common.parts)
        else:
            docker_dir = path / Path(directory)
        return f'COPY {directory} ./{docker_dir}'

    @property
    def contents(self) -> str:
        """Converts data into runnable Dockerfile text
        """
        lines = []
        lines.append(f'FROM {self.image}')

        for k, v in self.args.items():
            lines.append(f'ARG {k}="{v}"')

        for c in self.copy:
            lines.append(self.get_copy_command(c))

        return '\n'.join(lines)


def _push_stream_logger(log_generator: Generator[dict, None, None]) -> List[str]:
    last_status = None
    logs = []
    for log in log_generator:
        if 'aux' in log:
            logs.append(f'Pushed {log["aux"].get("Tag")} ({log["aux"].get("Digest")}), {log["aux"].get("Size")}bytes')
            break

        elif 'errorDetail' in log:
            raise RuntimeError(f'Failed to push to docker image: {log["errorDetail"]}')

        status = log.get('status', 'Unknown')
        if last_status == status:
            continue
        elif status == 'Unknown':
            logs.append(log)

        status_id = log.get('status_id', '')
        logs.append(f'Push status: {status} {status_id}')
        last_status = status

    return logs


class DockerImage:
    """Manage a docker image through the docker api
    """

    def __init__(self, repo: str, tag: str, client: Optional[docker.APIClient] = None):
        self.repo = repo
        self.tag = tag
        self.image = f"{repo}:{tag}"

        if client is None:
            client = get_docker_client()
        self.client: docker.APIClient = client

    def build(self, dockerfile: Dockerfile):
        """Builds a docker image using the dockerfile object provided
        """
        with NamedTemporaryFile('w', encoding='utf8') as temp:
            temp.write(dockerfile.contents)
            image_build, _ = self.client.images.build(dockerfile=dockerfile, tag=self.image, path=dockerfile.path)

        logger.debug(f'Docker image {image_build.id} created from {self.image}')

    def build_local_directories(self, directories: list, path: str) -> None:
        """Builds local directories into a docker image
        """

        # the first time you build an image you need to create the docker
        # manifest. For any subsequent builds, you'll want to use the image
        # name to do comparisons and avoid building the image from scratch.
        # See https://hub.docker.com/_/scratch
        from_image = 'scratch' if self.image not in get_image_tags(self.client) else self.image
        logger.debug(f'Creating local directory image from {from_image}')

        self.build(dockerfile=Dockerfile(image=from_image, copy=directories, path=path))

    def push(self, auth_config: Dict[str, Optional[str]]):
        """Pushes a docker image to a docker repo
        """
        args = {
            'repository': self.repo,
            'tag': self.tag,
            'auth_config': auth_config,
            # stream the push to catch any errors (not all raise an APIError)
            'stream': True,
            'decode': True,
        }
        for msg in _push_stream_logger(self.client.images.push(**args)):
            logger.debug(msg)

    def delete(self):
        """Delete the image locally
        """
        self.client.images.remove(self.image)
