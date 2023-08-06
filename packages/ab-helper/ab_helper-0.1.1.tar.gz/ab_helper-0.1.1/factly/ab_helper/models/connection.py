from typing import List, Optional

from pydantic import BaseModel, Json


class Schedule(BaseModel):
    units: int = 30
    timeUnit: str = "days"


class ResourceRequirements(BaseModel):
    cpu_request: str = ""
    cpu_limit: str = ""
    memory_request: str = ""
    memory_limit: str = ""


class Config(BaseModel):
    syncMode: str
    cursorField: List[str]
    destinationSyncMode: str
    primaryKey: List[List[str]]
    aliasName: str
    selected: bool


class SyncCatalogUc(BaseModel):
    streams: List[Json]


class CreateConnections(BaseModel):
    name: str
    namespaceDefinition: str = "source"
    namespaceFormat: str = "${SOURCE_NAMESPACE}"
    prefix: str = "airbyte_"
    sourceId: str
    destinationId: str
    operationIds: Optional[List[str]]
    syncCatalog: SyncCatalogUc
    schedule: Optional[Schedule]
    status: str
    resourceRequirements: ResourceRequirements
    sourceCatalogId: str


# Update Connection Configurations
class UpdateConnection(BaseModel):
    connectionId: str
    name: str
    namespaceDefinition: str = "source"
    namespaceFormat: str = "${SOURCE_NAMESPACE}"
    prefix: str = "airbyte_"
    operationIds: Optional[List[str]]
    syncCatalog: SyncCatalogUc
    schedule: Optional[Schedule]
    status: str
    resourceRequirements: ResourceRequirements
    sourceCatalogId: str
