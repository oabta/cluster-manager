import logging

import docker
from docker.models.containers import Container

from cluster_manager.core.docker import DockerExecutor
from cluster_manager.core.runtime import RuntimeConfig
from cluster_manager.utils.app import AppSettings, ClusterConfig, PSQLConfig, AppConfig

logger = logging.getLogger(__name__)

client = docker.from_env()


class Cluster:
    name: str
    containers: [Container]
    config: ClusterConfig | None
    is_initialized: bool

    def __init__(self, name: str):
        self.name = name
        self.containers = []
        self.docker = DockerExecutor(client, self)
        self.config = AppSettings.get_cluster_config(self.name)
        self.is_initialized = bool(self.config)

    def initialize(self, redis=False):
        if self.is_initialized:
            logger.info("already initialized")
            return
        self.config = AppSettings.make_cluster_config(self.name, redis)
        self.create()
        AppSettings.add_cluster_config(self.config)
        self.is_initialized = True

    def create(self):
        if db := self.config.env.db:
            container = self.docker.get_or_create_container(
                self.get_psql_runtime(db).model_dump()
            )
            self.containers.append(container)
        if app := self.config.env.app:
            container = self.docker.get_or_create_container(
                self.get_app_runtime(app).model_dump()
            )
            self.containers.append(container)
        if self.config.env.redis is not None:
            container = self.docker.get_or_create_container(
                self.get_redis_runtime().model_dump()
            )
            self.containers.append(container)

    def start(self):
        for service in ["app", "db", "redis"]:
            config = getattr(self.config.env, service)
            if config is None:
                continue
            name = "%s.%s" % (service, self.name)
            container = self.docker.get_container(name)
            if container.status == "running":
                logger.info("service [%s] already started", name)
                continue
            logger.info("starting service [%s]", name)
            container.start()
            self.containers.append(container)

    @staticmethod
    def with_name(name: str):
        return Cluster(name)

    def get_psql_runtime(self, db: PSQLConfig) -> RuntimeConfig:
        return RuntimeConfig(
            image=self.docker.get_image("postgres:alpine"),
            name="%s.%s" % ("db", self.name),
            hostname="%s.%s" % ("db", self.name),
            environment=db.model_dump(),
            ports={"5432": 5432},
            network=self.name,
        )

    def get_app_runtime(self, db: AppConfig) -> RuntimeConfig:
        return RuntimeConfig(
            image=self.docker.get_image("hello-world"),
            name="%s.%s" % ("app", self.name),
            hostname="%s.%s" % ("app", self.name),
            environment=db.model_dump(),
            network=self.name,
        )

    def get_redis_runtime(self) -> RuntimeConfig:
        return RuntimeConfig(
            image=self.docker.get_image("redis:alpine"),
            name="%s.%s" % ("redis", self.name),
            hostname="%s.%s" % ("redis", self.name),
            network=self.name,
        )
