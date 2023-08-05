from enum import Enum


class ResourceType(Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    REDSHIFT = "redshift"
    URL = "url"
    S3 = "s3"
    MONGODB = "mongodb"
    ELASTICSEARCH = "elasticsearch"
    SNOWFLAKE = "snowflakedb"
    BIGQUERY = "bigquery"
    SQLSERVER = "sqlserver"
    COSMODB = "cosmodb"


class MeroxaApiResponse(object):
    def __init__(self, *args, **kwargs):
        ...


class ClientOptions:
    def __init__(self, auth: str, url: str, timeout=0.0):
        self.auth = auth
        self.timeout = timeout
        self.url = url


class EnvironmentIdentifier:
    def __init__(self, name=None, uuid=None):
        self.name = name
        self.uuid = uuid

    def repr_json(self):
        return dict(name=self.name) if self.name is not None else dict(uuid=self.uuid)


class EntityIdentifier:
    def __init__(self, name=None, uuid=None):
        self.name = name
        self.uuid = uuid

    def repr_json(self):
        return dict(name=self.name) if self.name is not None else dict(uuid=self.uuid)
