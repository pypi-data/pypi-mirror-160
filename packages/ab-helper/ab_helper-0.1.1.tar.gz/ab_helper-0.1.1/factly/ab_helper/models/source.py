from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

# Enums


class Format(BaseModel):
    encoding: str = "utf-8"
    filetype: str = "csv"
    delimiter: str = ","
    block_size: int = 1000000
    quote_char: str = '"'
    double_quote: bool = True
    infer_datatypes: bool = True
    advanced_options: str = "{}"
    newlines_in_values: bool = False
    additional_reader_options: str = "{}"


class Provider(BaseModel):
    bucket: str
    use_ssl: bool
    endpoint: str
    path_prefix: str
    aws_access_key_id: str
    aws_secret_access_key: str


class ConnectionConfiguration(BaseModel):
    # user: str = "techteam@factly.in"
    format: Format
    schema_: str = Field("{}", alias="schema")
    dataset: str
    provider: Provider
    path_pattern: str = "**"


class SourceConfigurationTemplate(BaseModel):
    workspaceId: Optional[str]
    sourceDefinitionId: Optional[str]
    connectionConfiguration: Optional[ConnectionConfiguration]
    name: Optional[str]


class UpdateSourceConfigurationTemplate(BaseModel):
    sourceId: str
    connectionConfiguration: ConnectionConfiguration
    name: str
