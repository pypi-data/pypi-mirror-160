""" MCLI Integration Local Directories """
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob

logger = logging.getLogger(__name__)


@dataclass
class MCLILocalIntegration(MCLIIntegration):
    """Local Directories Integration
    """

    directories: Union[str, List[str]]
    docker_path: Optional[str] = None

    def _validate_directories_exist(self) -> None:
        for directory in self.directories:
            path = Path(directory).expanduser().absolute()
            if not path.exists():
                raise NotADirectoryError(f'Could not find directory in local directories integration: {path}')

            if not path.is_dir():
                raise NotADirectoryError(
                    f'Expected {path} in local directories integration to be a directory, but found a file instead')

    def __post_init__(self):
        if isinstance(self.directories, str):
            self.directories = [self.directories]
        self._validate_directories_exist()

    def build_to_docker(self) -> bool:
        raise NotImplementedError('See HEK762')

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        """Add a integration to a job
        """
        logger.warning(
            'Local directories can only be added as part of a Docker image. Please specify `build_docker` in the yaml')
        return True  # still return True so there isn't duplicated warnings
