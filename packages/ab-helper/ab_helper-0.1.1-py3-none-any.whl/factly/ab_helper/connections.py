import json
import logging
import logging.config
from typing import Any, Dict, List

import requests

from .core.configs import Settings
from .destination import _list_existing_definition_in_workspace
from .models.connection import (
    CreateConnections,
    ResourceRequirements,
    SyncCatalogUc,
    UpdateConnection,
)
from .models.operation import (
    Normalization,
    OperationCreate,
    OperatorConfiguration,
)
from .source import _list_existing_sources_in_workspace
from .utils import check_health, find_workspace_id_by_slug

settings = Settings()

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def _list_existing_connection_in_workspace(
    airbyte_host_url: str,
    list_connection_api: str,
    workspace_id: str,
    headers: List[Dict[str, Any]],
):
    connection_list_response = requests.post(
        url=f"{airbyte_host_url}{list_connection_api}",
        data=json.dumps({"workspaceId": workspace_id}),
        headers=headers,
    )
    connection_list_response.raise_for_status()
    connection_list_response_json = connection_list_response.json()["connections"]
    connection_name_mappings = {
        connection["name"]: connection for connection in connection_list_response_json
    }

    return connection_name_mappings


def _get_source_schema_from_id(
    airbyte_host_url: str,
    discover_source_schema_api: str,
    source_id: str,
    disable_cache: bool,
    headers: Dict[str, Any],
):
    logger.debug(f"Requesting : {airbyte_host_url}{discover_source_schema_api}")
    logger.debug(f"SourceID : {source_id}")
    source_schema_response = requests.post(
        url=f"{airbyte_host_url}{discover_source_schema_api}",
        data=json.dumps(
            {
                "sourceId": source_id,
                "disable_cache": disable_cache,
            }
        ),
        headers=headers,
    )
    source_schema_response.raise_for_status()
    source_schema_json = source_schema_response.json()
    logger.debug(source_schema_json)
    source_schema_streams = source_schema_json["catalog"]["streams"][0]
    source_schema_catalog_id = source_schema_json["catalogId"]
    logger.info(f"Source catalog Id : {source_schema_catalog_id}")
    logger.info("Source schema received..")
    return {
        "source_schema_streams": source_schema_streams,
        "source_schema_catalog_id": source_schema_catalog_id,
    }


def _create_operation_for_connection(
    airbyte_host_url: str,
    create_operation_api: str,
    workspace_id: str,
    source_name: str,
    operator_type: str,
    normalize_option: str,
    headers: Dict[str, Any],
):
    operation_configuration = OperationCreate(
        workspaceId=workspace_id,
        name=source_name,
        operatorConfiguration=OperatorConfiguration(
            operatorType=operator_type,
            normalization=Normalization(option=normalize_option),
        ),
    )

    operation_response = requests.post(
        url=f"{airbyte_host_url}{create_operation_api}",
        data=operation_configuration.json(
            exclude_defaults=False, exclude_unset=False, by_alias=True
        ),
        headers=headers,
    )
    operation_response.raise_for_status()
    operation_id = operation_response.json()["operationId"]
    return operation_id


def _get_operation_id_for_connection(
    connection_id: str,
    airbyte_host_url: str,
    list_operation_api: str,
    headers: Dict[str, Any],
):

    return_operation_id = requests.post(
        url=f"{airbyte_host_url}{list_operation_api}",
        data=json.dumps({"connectionId": connection_id}),
        headers=headers,
    )
    return_operation_id.raise_for_status()
    operation_ids = [
        operation["operationId"]
        for operation in return_operation_id.json()["operations"]
    ]
    return operation_ids


def create_or_update_connection(
    airbyte_host_url: str,
    workspace_name: str,
    dataset_details: List[Dict[str, Any]],
    health_check_api=settings.API_AIRBYTE_HEALTH_CHECK,
    find_workspace_id_by_slug_api=settings.API_FIND_WORKSPACE_BY_SLUG,
    list_source_api=settings.API_LIST_SOURCES,
    list_destination_api=settings.API_LIST_DESTINATION,
    list_connection_api=settings.API_LIST_CONNECTION,
    discover_source_schema_api=settings.API_DISCOVER_SOURCE_SCHEMA,
    create_operation_api=settings.API_CREATE_OPERATION,
    create_connection_api=settings.API_CREATE_CONNECTION,
    list_operation_api=settings.API_LIST_OPERATION,
    update_connection_api=settings.API_UPDATE_CONNECTION,
    disable_cache=settings.DISABLE_SOURCE_SCHEMA_CACHE,
    operator_type=settings.OPERATOR_TYPE,
    normalize_option=settings.NORMALIZE_OPTION,
    headers=settings.HEADERS,
):
    # check the health
    check_health(
        airbyte_host_url=airbyte_host_url,
        health_check_api=health_check_api,
        headers=headers,
    )

    # workspace Id is required for further operations
    workspace_id = find_workspace_id_by_slug(
        airbyte_host_api=airbyte_host_url,
        find_workspace_by_slug_api=find_workspace_id_by_slug_api,
        workspace_name=workspace_name,
        headers=headers,
    )

    existing_sources = _list_existing_sources_in_workspace(
        airbyte_host_url=airbyte_host_url,
        list_source_api=list_source_api,
        workspace_id=workspace_id,
        headers=headers,
    )

    existing_destinations = _list_existing_definition_in_workspace(
        airbyte_host_url=airbyte_host_url,
        list_destination_api=list_destination_api,
        workspace_id=workspace_id,
        headers=headers,
    )

    existing_connection = _list_existing_connection_in_workspace(
        airbyte_host_url=airbyte_host_url,
        list_connection_api=list_connection_api,
        workspace_id=workspace_id,
        headers=headers,
    )
    logger.debug(existing_sources)
    logger.debug(existing_destinations)
    logger.debug(existing_connection)
    for dataset_detail in dataset_details:
        logger.info(f"Building connection for : {dataset_detail['connection_name']}")

        # discover source schema
        source_schema_details = _get_source_schema_from_id(
            airbyte_host_url=airbyte_host_url,
            discover_source_schema_api=discover_source_schema_api,
            source_id=existing_sources[dataset_detail["source_name"]],
            disable_cache=disable_cache,
            headers=headers,
        )

        if dataset_detail["connection_name"] not in existing_connection:

            # This will lead to create a new connection
            # First step is to create a new operation
            operation_id = _create_operation_for_connection(
                airbyte_host_url=airbyte_host_url,
                create_operation_api=create_operation_api,
                workspace_id=workspace_id,
                source_name=dataset_detail["source_name"],
                operator_type=operator_type,
                normalize_option=normalize_option,
                headers=headers,
            )

            create_connection_configurations = CreateConnections(
                name=dataset_detail["connection_name"],
                sourceId=existing_sources[dataset_detail["source_name"]],
                destinationId=existing_destinations[dataset_detail["destination_name"]],
                operationIds=[operation_id],
                syncCatalog=SyncCatalogUc(
                    streams=[json.dumps(source_schema_details["source_schema_streams"])]
                ),
                status=settings.DEFAULT_CONNECTION_STATUS,
                resourceRequirements=ResourceRequirements(),
                sourceCatalogId=source_schema_details["source_schema_catalog_id"],
            )

            # main request that will create connection
            create_connection_response = requests.post(
                url=f"{airbyte_host_url}{create_connection_api}",
                data=create_connection_configurations.json(
                    exclude_defaults=False, exclude_unset=False, by_alias=True
                ),
                headers=settings.HEADERS,
            )
            create_connection_response.raise_for_status()
            logger.info(
                f"Connection {dataset_detail['connection_name']} created : {create_connection_response.json()['connectionId']}"
            )

        else:

            operation_id = _get_operation_id_for_connection(
                connection_id=existing_connection[
                    dataset_detail["connection_name"]
                ].get("connectionId"),
                list_operation_api=list_operation_api,
                airbyte_host_url=airbyte_host_url,
                headers=headers,
            )

            update_connection_configuration = UpdateConnection(
                connectionId=existing_connection[dataset_detail["connection_name"]].get(
                    "connectionId"
                ),
                name=dataset_detail["connection_name"],
                sourceId=existing_sources[dataset_detail["source_name"]],
                destinationId=existing_destinations[dataset_detail["destination_name"]],
                operationIds=operation_id,
                syncCatalog=SyncCatalogUc(
                    streams=[json.dumps(source_schema_details["source_schema_streams"])]
                ),
                status=settings.DEFAULT_CONNECTION_STATUS,
                resourceRequirements=ResourceRequirements(),
                sourceCatalogId=source_schema_details["source_schema_catalog_id"],
            )

            # main request to update a connection
            update_connection_response = requests.post(
                url=f"{airbyte_host_url}{update_connection_api}",
                data=update_connection_configuration.json(
                    exclude_defaults=False, exclude_unset=False, by_alias=True
                ),
                headers=settings.HEADERS,
            )
            update_connection_response.raise_for_status()
            logger.info(
                f"Connection {dataset_detail['connection_name']} updated : {update_connection_response.json()['connectionId']}"
            )
