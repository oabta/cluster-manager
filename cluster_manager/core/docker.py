import logging
from contextlib import suppress
from typing import Protocol

from docker import DockerClient
from docker.errors import APIError
from docker.models.containers import Container
from docker.models.images import Image
from docker.models.networks import Network

logger = logging.getLogger(__name__)


class Cluster(Protocol):
    name: str


class DockerExecutor:
    def __init__(self, client: DockerClient, cluster: Cluster):
        self.client = client
        self.cluster = cluster

    def get_or_create_container(self, kwargs: dict) -> Container | None:
        try:
            logger.info("creating container [%s]", kwargs.get('name'))
            return self.client.containers.create(**kwargs)
        except APIError as e:
            self.client.containers.get(kwargs.get('name'))

    def get_container(self, name: str) -> Container | None:
        with suppress(APIError):
            return self.client.containers.get(name)

    def run_container(self, kwargs: dict) -> Container:
        logger.info("running container [%s]", kwargs.get('name'))
        return self.client.containers.run(**kwargs)

    def get_network(self) -> Network:
        return self.client.networks.get(self.cluster.name)

    def get_or_create_network(self) -> Network | None:
        try:
            return self.client.networks.create(self.cluster.name)
        except APIError:
            with suppress(APIError):
                return self.get_network()

    def get_image(self, image) -> Image | None:
        logger.info("pulling docker image [%s]", image)
        with suppress(APIError):
            return self.client.images.pull(image)
