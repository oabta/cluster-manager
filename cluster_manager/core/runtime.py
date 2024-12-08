from docker.models.images import Image
from pydantic import BaseModel


class RuntimeConfig(BaseModel):
    name: str
    image: Image
    hostname: str
    network: str

    environment: dict[str, str | int] | list[str] = None
    entrypoint: str | list[str] | None = None
    ports: dict[str, int | list[int] | tuple[str, int] | None] | None = None
    volumes: dict[str, str] | list[str] | None = None
    volumes_from: list[str] | None = None
    working_dir: str | None = None

    class Config:
        arbitrary_types_allowed = True
