import json
import logging
import logging.config
import os
from typing import Any, Dict, List

import requests

from .core.configs import Settings
from .models.source import (
    ConnectionConfiguration,
    Format,
    Provider,
    SourceConfigurationTemplate,
    UpdateSourceConfigurationTemplate,
)
from .utils import check_health, find_workspace_id_by_slug

settings = Settings()

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def _get_source_definition_id(
    workspace_id: str,
    airbyte_host_url: str,
    source_definition_api: str,
    headers: Dict[str, Any],
):
    sd_response = requests.post(
        url=f"{airbyte_host_url}{source_definition_api}",
        data=json.dumps({"workspaceId": workspace_id}),
        headers=headers,
    )
    sd_response.raise_for_status()

    # STEP 1 : Get Source definition for S3 source storage

    try:
        s3_source_definition_id = [
            definition["sourceDefinitionId"]
            for definition in sd_response.json()["sourceDefinitions"]
            if definition["name"] == "S3"
        ][0]
    except IndexError as ie:
        logger.exception(
            f"No source definition found in s3 for current workspaceID : {workspace_id} : {ie}"
        )
        raise IndexError
    else:
        logger.info(f"Source definition for S3: {s3_source_definition_id}")
        return s3_source_definition_id


def _list_existing_sources_in_workspace(
    airbyte_host_url: str,
    list_source_api: str,
    workspace_id: str,
    headers: Dict[str, Any],
):
    source_list_response = requests.post(
        url=f"{airbyte_host_url}{list_source_api}",
        data=json.dumps({"workspaceId": workspace_id}),
        headers=headers,
    )
    source_list_response.raise_for_status()

    existing_source = {
        source["name"]: source["sourceId"]
        for source in source_list_response.json()["sources"]
    }

    return existing_source


def create_or_update_source(
    airbyte_host_url: str,
    workspace_name: str,
    dataset_details: List[Dict[str, Any]],
    health_check_api=settings.API_AIRBYTE_HEALTH_CHECK,
    find_workspace_id_by_slug_api=settings.API_FIND_WORKSPACE_BY_SLUG,
    get_source_definition_api=settings.API_SOURCE_DEFINITION,
    list_source_api=settings.API_LIST_SOURCES,
    create_source_api=settings.API_CREATE_SOURCES,
    update_source_api=settings.API_UPDATE_SOURCE,
    check_source_connection_api=settings.API_CHECK_CONNECTION_SOURCE,
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

    s3_source_definition_id = _get_source_definition_id(
        workspace_id=workspace_id,
        airbyte_host_url=airbyte_host_url,
        source_definition_api=get_source_definition_api,
        headers=headers,
    )

    existing_sources = _list_existing_sources_in_workspace(
        workspace_id=workspace_id,
        airbyte_host_url=airbyte_host_url,
        list_source_api=list_source_api,
        headers=headers,
    )

    for idx, dataset_detail in enumerate(dataset_details, 1):
        logger.debug(f"Source : {dataset_detail['source_name']}")

        if dataset_detail["source_name"] not in existing_sources.keys():
            # create new source as it does not exist
            # generate configuration
            source_configuration = SourceConfigurationTemplate(
                workspaceId=workspace_id,
                sourceDefinitionId=s3_source_definition_id,
                name=dataset_detail["source_name"],
                connectionConfiguration=ConnectionConfiguration(
                    provider=Provider(
                        bucket=settings.S3_BUCKET,
                        use_ssl=settings.S3_USE_SSL,
                        endpoint=os.environ.get("S3_ENDPOINT"),
                        path_prefix=dataset_detail["path_prefix"],
                        aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
                        aws_secret_access_key=os.environ.get("S3_SECRET_KEY"),
                    ),
                    format=Format(),
                    dataset=dataset_detail["source_name"],
                    path_pattern=dataset_detail["path_pattern"],
                ),
            )

            # create source
            source_response = requests.post(
                url=f"{airbyte_host_url}{create_source_api}",
                data=source_configuration.json(
                    exclude_defaults=False, exclude_unset=False, by_alias=True
                ),
                headers=settings.HEADERS,
            )
            source_response.raise_for_status()
            logger.info(f"Source {source_response.json()['sourceId']}: Created")
        else:
            # update the source if there are any change
            source_update_configuration = UpdateSourceConfigurationTemplate(
                sourceId=existing_sources[dataset_detail["source_name"]],
                connectionConfiguration=ConnectionConfiguration(
                    provider=Provider(
                        bucket=settings.S3_BUCKET,
                        use_ssl=False,
                        endpoint=os.environ.get("S3_ENDPOINT"),
                        path_prefix=dataset_detail["path_prefix"],
                        aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
                        aws_secret_access_key=os.environ.get("S3_SECRET_KEY"),
                    ),
                    format=Format(),
                    dataset=dataset_detail["source_name"],
                    path_pattern=dataset_detail["path_pattern"],
                ),
                name=dataset_detail["source_name"],
            )
            source_response = requests.post(
                url=f"{airbyte_host_url}{update_source_api}",
                data=source_update_configuration.json(
                    exclude_defaults=False, exclude_unset=False, by_alias=True
                ),
                headers=settings.HEADERS,
            )
            logger.info(f"Source {source_response.json()['sourceId']}: Updated")

        # check if the source are actually
        check_response = requests.post(
            url=f"{airbyte_host_url}{check_source_connection_api}",
            data=json.dumps({"sourceId": source_response.json()["sourceId"]}),
            headers=settings.HEADERS,
        )
        json_check_response = check_response.json()
        logger.info(f"Connection status: {json_check_response['status']}")
        logger.info(f"Completed sources : {idx}/{len(dataset_details)}")
