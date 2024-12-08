import json
import logging
from contextlib import suppress
from pathlib import Path

from appdirs import user_config_dir
from pydantic import BaseModel, Field

from cluster_manager.utils.crypto import generate_password

logger = logging.getLogger(__name__)


class PSQLConfig(BaseModel):
    POSTGRES_PASSWORD: str = Field(default_factory=lambda: generate_password())
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "postgres"


class AppConfig(BaseModel):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str | int


class ServicesConfig(BaseModel):
    app: AppConfig
    db: PSQLConfig
    redis: dict[str, str | int] | None = None


class ClusterConfig(BaseModel):
    name: str
    env: ServicesConfig


class _AppSettings:
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.app_author = "Oabta PTY (LTD)"
        self.clusters = self.load_clusters()

    def config_dir(self) -> Path:
        _dir = Path(user_config_dir(
            self.app_name,
            self.app_author,
        ))
        _dir.mkdir(parents=True, exist_ok=True)
        return _dir

    def load_clusters(self) -> [ClusterConfig]:
        file = self.config_dir().joinpath("clusters.json")
        if not file.exists():
            file.write_text(json.dumps([], indent=2))
        data = json.loads(file.read_text())
        return [ClusterConfig(**cluster) for cluster in data]

    @staticmethod
    def make_cluster_config(name: str, redis=False):
        psql = PSQLConfig()
        app = AppConfig(
            DB_HOST="%s.%s" % ("db", name),
            DB_NAME=psql.POSTGRES_DB,
            DB_USER=psql.POSTGRES_USER,
            DB_PASSWORD=psql.POSTGRES_PASSWORD,
            DB_PORT=5432,
        )
        return ClusterConfig(
            name=name,
            env=ServicesConfig(app=app, db=psql, redis={} if redis else None),
        )

    def add_cluster_config(self, config: ClusterConfig):
        self.clusters.append(config)

    def get_cluster_config(self, name: str) -> ClusterConfig | None:
        def match(cluster: ClusterConfig) -> bool:
            return cluster.name == name

        with suppress(IndexError):
            matches = list(filter(match, self.clusters))
            return matches.pop()

    def __del__(self):
        self.config_dir().joinpath("clusters.json").write_text(json.dumps([
            cluster.model_dump() for cluster in self.clusters
        ], indent=2))


AppSettings = _AppSettings("cluster-manager")
