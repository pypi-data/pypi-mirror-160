from typing import Optional

from confluent_kafka.schema_registry import SchemaRegistryClient, SchemaRegistryError

from kaskade.config import Config
from kaskade.kafka.mappers import metadata_to_schema
from kaskade.kafka.models import Schema

AVRO = "AVRO"
PROTOBUF = "PROTOBUF"
JSON = "JSON"


class SchemaService:
    def __init__(self, config: Config):
        if config is None or config.schema_registry is None:
            raise Exception("Schema registry config not found")

        self.config = config
        self.schema_registry_config = self.config.schema_registry.copy()
        self.schema_registry_client = SchemaRegistryClient(self.schema_registry_config)
        self.check_schema_registry()

    def check_schema_registry(self) -> None:
        try:
            self.schema_registry_client._rest_client.get("schemas/types")
        except Exception:
            raise Exception(
                f"Error connecting to schema registry at {self.schema_registry_config['url']}"
            )

    def get_schema(self, id: int) -> Optional[Schema]:
        try:
            metadata = self.schema_registry_client.get_schema(id)
            if metadata is not None:
                schema = metadata_to_schema(metadata)
                schema.id = id
                return schema
            else:
                return None
        except SchemaRegistryError as ex:
            if ex.http_status_code == 404:
                return None
            else:
                raise ex

    def close(self) -> None:
        self.schema_registry_client._rest_client.session.close()


if __name__ == "__main__":
    from rich import print

    config = Config("kaskade.yml")
    client = SchemaService(config)
    client.check_schema_registry()

    schema = client.get_schema(1)
    client.close()

    if schema is not None:
        print(schema.type)
        print(schema.data)

    print(schema)
