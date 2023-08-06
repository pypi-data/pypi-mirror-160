import json
import logging
import logging.config
import os
from typing import Any, Dict, List

import requests

from .core.configs import Settings
from .models.destination import (
    DestinationConfigurationTemplate,
    DestinationConnectionConfiguration,
    DestinationCredentials,
    DestinationLoadingMethod,
    UpdateDestinationConfigurationTemplate,
)
from .utils import check_health, find_workspace_id_by_slug

settings = Settings()

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def _get_destination_definition_id(
    workspace_id: str,
    airbyte_host_url: str,
    destination_definition_api: str,
    headers: Dict[str, Any],
):
    dd_response = requests.post(
        url=f"{airbyte_host_url}{destination_definition_api}",
        data=json.dumps({"workspaceId": workspace_id}),
        headers=headers,
    )
    dd_response.raise_for_status()

    try:
        snowflake_destination_definition_id = [
            definition["destinationDefinitionId"]
            for definition in dd_response.json()["destinationDefinitions"]
            if definition["name"] == "Snowflake"
        ][0]
    except IndexError as ie:
        logger.exception(
            f"No Destination definition found in Snowflake for current workspaceID : {workspace_id} : {ie}"
        )
        raise IndexError
    else:
        logger.info(
            f"Destination definition for Snowflake: {snowflake_destination_definition_id}"
        )
        return snowflake_destination_definition_id


def _list_existing_definition_in_workspace(
    airbyte_host_url: str,
    list_destination_api: str,
    workspace_id: str,
    headers: Dict[str, Any],
):
    destination_list_response = requests.post(
        url=f"{airbyte_host_url}{list_destination_api}",
        data=json.dumps({"workspaceId": workspace_id}),
        headers=headers,
    )
    destination_list_response.raise_for_status()
    existing_destination = {
        destination["name"]: destination["destinationId"]
        for destination in destination_list_response.json()["destinations"]
    }

    return existing_destination


def create_or_update_destination(
    airbyte_host_url: str,
    workspace_name: str,
    dataset_details: List[Dict[str, Any]],
    health_check_api=settings.API_AIRBYTE_HEALTH_CHECK,
    find_workspace_id_by_slug_api=settings.API_FIND_WORKSPACE_BY_SLUG,
    destination_definition_api=settings.API_DESTINATION_DEFINITION,
    list_destination_api=settings.API_LIST_DESTINATION,
    create_destination_api=settings.API_CREATE_DESTINATION,
    update_destination_api=settings.API_UPDATE_DESTINATION,
    check_destination_connection_api=settings.API_CHECK_DESTINATION_CONNECTION,
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

    snowflake_destination_definition_id = _get_destination_definition_id(
        workspace_id=workspace_id,
        airbyte_host_url=airbyte_host_url,
        destination_definition_api=destination_definition_api,
        headers=headers,
    )

    existing_destination = _list_existing_definition_in_workspace(
        airbyte_host_url=airbyte_host_url,
        list_destination_api=list_destination_api,
        workspace_id=workspace_id,
        headers=headers,
    )

    for idx, dataset_detail in enumerate(dataset_details, 1):
        logger.debug(f"Destination : {dataset_detail['destination_name']}")

        if dataset_detail["destination_name"] not in existing_destination.keys():
            # create new destination as it does not existing
            # general configuration

            destination_configuration = DestinationConfigurationTemplate(
                workspaceId=workspace_id,
                destinationDefinitionId=snowflake_destination_definition_id,
                name=dataset_detail["destination_name"],
                connectionConfiguration=DestinationConnectionConfiguration(
                    host=os.environ.get("SNOWFLAKE_HOST"),
                    role=os.environ.get("SNOWFLAKE_ROLE"),
                    schema_=os.environ.get("SNOWFLAKE_SCHEMA"),
                    database=os.environ.get("SNOWFLAKE_DATABASE"),
                    username=os.environ.get("SNOWFLAKE_USERNAME"),
                    warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
                    credentials=DestinationCredentials(
                        password=os.environ.get("SNOWFLAKE_USER_PASSWORD")
                    ),
                    loading_method=DestinationLoadingMethod(
                        method=os.environ.get("SNOWFLAKE_LOADING_METHOD")
                    ),
                ),
            )

            # create new destination
            destination_response = requests.post(
                url=f"{airbyte_host_url}{create_destination_api}",
                data=destination_configuration.json(
                    exclude_defaults=False, exclude_unset=False, by_alias=True
                ),
                headers=headers,
            )
            destination_response.raise_for_status()
            logger.info(
                f"Destination {destination_response.json()['destinationId']}: Created"
            )
        else:
            destination_update_configuration = UpdateDestinationConfigurationTemplate(
                name=dataset_detail["destination_name"],
                destinationId=existing_destination[dataset_detail["destination_name"]],
                connectionConfiguration=DestinationConnectionConfiguration(
                    host=os.environ.get("SNOWFLAKE_HOST"),
                    role=os.environ.get("SNOWFLAKE_ROLE"),
                    schema_=os.environ.get("SNOWFLAKE_SCHEMA"),
                    database=os.environ.get("SNOWFLAKE_DATABASE"),
                    username=os.environ.get("SNOWFLAKE_USERNAME"),
                    warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
                    credentials=DestinationCredentials(
                        password=os.environ.get("SNOWFLAKE_USER_PASSWORD")
                    ),
                    loading_method=DestinationLoadingMethod(
                        method=os.environ.get("SNOWFLAKE_LOADING_METHOD")
                    ),
                ),
            )

            destination_response = requests.post(
                url=f"{airbyte_host_url}{update_destination_api}",
                data=destination_update_configuration.json(
                    exclude_defaults=False, exclude_unset=False, by_alias=True
                ),
                headers=headers,
            )
            destination_response.raise_for_status()
            logger.info(
                f"Destination {destination_response.json()['destinationId']}: Updated"
            )

        # check if the source are actually
        check_response = requests.post(
            url=f"{airbyte_host_url}{check_destination_connection_api}",
            data=json.dumps(
                {"destinationId": destination_response.json()["destinationId"]}
            ),
            headers=settings.HEADERS,
        )
        json_check_response = check_response.json()
        logger.info(f"Connection status: {json_check_response['status']}")
        logger.info(f"Destination Handled : {idx}/{len(dataset_details)}")
