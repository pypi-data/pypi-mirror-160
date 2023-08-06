import json
import logging
import logging.config

import requests

from .core.configs import Settings
from .utils import check_health, find_workspace_id_by_slug

settings = Settings()

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def run_manual_sync(
    airbyte_host_url: str,
    workspace_name: str,
    health_check_api=settings.API_AIRBYTE_HEALTH_CHECK,
    find_workspace_id_by_slug_api=settings.API_FIND_WORKSPACE_BY_SLUG,
    list_connection_api=settings.API_LIST_CONNECTION,
    run_sync_api=settings.API_RUN_SYNC,
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

    connections = requests.post(
        url=f"{airbyte_host_url}{list_connection_api}",
        data=json.dumps({"workspaceId": workspace_id}),
        headers=headers,
    )
    connections.raise_for_status()
    for connection in connections.json()["connections"]:
        try:
            run_response = requests.post(
                url=f"{airbyte_host_url}{run_sync_api}",
                data=json.dumps({"connectionId": connection["connectionId"]}),
                headers=headers,
            )
            run_response.raise_for_status()
        except Exception as e:
            logger.exception(f"Error {connection['connectionId']} : {e}")
