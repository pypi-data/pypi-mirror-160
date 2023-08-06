from typing import Dict

from pydantic import BaseSettings


class Settings(BaseSettings):

    # Argo details
    ARGO_SERVER_HOST: str = ""

    API_AIRBYTE_URL: str = "http://localhost:8001/api"
    LOGGER_NAME: str = "abHelper"
    LOGGER_DEBUG_LEVEL: str = "DEBUG"
    HEADERS: Dict = {"content-type": "application/json"}

    # health check api
    API_AIRBYTE_HEALTH_CHECK: str = "/v1/health"

    # workspace
    API_LIST_WORKSPACES: str = "/v1/workspaces/list"
    API_FIND_WORKSPACE_BY_SLUG: str = "/v1/workspaces/get_by_slug"
    API_CREATE_WORKSPACE: str = "/v1/workspaces/create"
    API_UPDATE_WORKSPACE: str = "/v1/workspaces/update"

    # source and source definition
    API_SOURCE_DEFINITION: str = "/v1/source_definitions/list_for_workspace"
    API_LIST_SOURCES: str = "/v1/sources/list"
    API_CREATE_SOURCES: str = "/v1/sources/create"
    API_UPDATE_SOURCE: str = "/v1/sources/update"
    API_CHECK_CONNECTION_SOURCE: str = "/v1/sources/check_connection"
    S3_ENDPOINT: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = ""
    S3_USE_SSL: str = False

    # destination and destination definition
    API_DESTINATION_DEFINITION: str = "/v1/destination_definitions/list"
    API_LIST_DESTINATION: str = "/v1/destinations/list"
    API_CREATE_DESTINATION: str = "/v1/destinations/create"
    API_UPDATE_DESTINATION: str = "/v1/destinations/update"
    API_CHECK_DESTINATION_CONNECTION: str = "/v1/destinations/check_connection"
    SNOWFLAKE_USERNAME: str = "AIRBYTE_USER"
    SNOWFLAKE_HOST: str = ""
    SNOWFLAKE_ROLE: str = ""
    SNOWFLAKE_SCHEMA: str = ""
    SNOWFLAKE_DATABASE: str = ""
    SNOWFLAKE_WAREHOUSE: str = ""
    SNOWFLAKE_USER_PASSWORD: str = ""
    SNOWFLAKE_LOADING_METHOD: str = ""
    AIRBYTE_WORKSPACE_NAME: str = ""

    # connections
    API_LIST_CONNECTION: str = "/v1/connections/list"
    API_CREATE_CONNECTION: str = "/v1/connections/create"
    API_UPDATE_CONNECTION: str = "/v1/connections/update"
    API_DISCOVER_SOURCE_SCHEMA: str = "/v1/sources/discover_schema"
    API_RETURN_OPERATION: str = "/v1/operations/list"
    API_CREATE_OPERATION: str = "/v1/operations/create"
    API_LIST_OPERATION: str = "/v1/operations/list"
    DEFAULT_CONNECTION_STATUS: str = "active"

    # sync mechanism
    API_RUN_SYNC: str = "/v1/connections/sync"

    # Airbyte Connection
    DISABLE_SOURCE_SCHEMA_CACHE: bool = False
    OPERATOR_TYPE: str = "normalization"
    NORMALIZE_OPTION: str = "basic"

    class config:
        env_file = ".env"
