from pydantic import BaseModel, Field


class DestinationCredentials(BaseModel):
    password: str


class DestinationLoadingMethod(BaseModel):
    method: str


class DestinationConnectionConfiguration(BaseModel):
    host: str = "424892c4-daac-4491-b35d-c6688ba547ba"
    role: str = "AIRBYTE_ROLE"
    schema_: str = Field("AIRBYTE_SCHEMA", alias="schema")
    database: str = "AIRBYTE_DATABASE"
    username: str = "AIRBYTE_USER"
    warehouse: str = "AIRBYTE_WAREHOUSE"
    credentials: DestinationCredentials
    loading_method: DestinationLoadingMethod


class DestinationConfigurationTemplate(BaseModel):
    destinationDefinitionId: str
    workspaceId: str
    connectionConfiguration: DestinationConnectionConfiguration
    name: str


class UpdateDestinationConfigurationTemplate(BaseModel):

    destinationId: str
    connectionConfiguration: DestinationConnectionConfiguration
    name: str
