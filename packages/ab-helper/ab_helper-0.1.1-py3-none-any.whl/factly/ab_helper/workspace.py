import json
import logging
import logging.config

import requests

from .core.configs import Settings
from .models.workspace import (
    CreateWorkspace,
    Notification,
    SlackConfiguration,
    UpdateWorkspace,
)
from .utils import check_health

settings = Settings()

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def create_or_update_workspace(
    airbyte_host_url: str,
    workspace_name: str,
    health_check_api=settings.API_AIRBYTE_HEALTH_CHECK,
    workspace_name_by_slug_api=settings.API_FIND_WORKSPACE_BY_SLUG,
    create_workspace_api=settings.API_CREATE_WORKSPACE,
    update_workspace_api=settings.API_UPDATE_WORKSPACE,
    headers=settings.HEADERS,
):

    # check the health
    check_health(
        airbyte_host_url=airbyte_host_url,
        health_check_api=health_check_api,
        headers=headers,
    )

    # create workspace model
    workspace_create_configuration = CreateWorkspace(
        name=workspace_name,
        notifications=[Notification(slackConfiguration=SlackConfiguration())],
    )

    # list out if the workspace already exists

    response = requests.post(
        url=f"{airbyte_host_url}{workspace_name_by_slug_api}",
        data=json.dumps({"slug": workspace_name}),
        headers=headers,
    )
    json_response = response.json()

    if response.status_code == 422:
        # input field validation failed
        response.raise_for_status()

    if response.status_code == 404:
        # workspace does not exist , thus create one
        logger.warning(f"Workspace {workspace_name} exists : False")
        logger.debug(f"Creating Workspace : {workspace_name}")
        response = requests.post(
            url=f"{airbyte_host_url}{create_workspace_api}",
            data=workspace_create_configuration.json(
                exclude_defaults=False, exclude_unset=False, by_alias=True
            ),
            headers=headers,
        )
        response.raise_for_status()
        json_response = response.json()
        workspace_id = json_response["workspaceId"]
        logger.info(f"Workspace {workspace_name} created with ID : {workspace_id}")
        return workspace_id
    if response.status_code == 200:
        workspace_id = json_response["workspaceId"]
        logger.info(f"Workspace {workspace_name} exists : {workspace_id}")
        logger.info("Checking for updates...")

        update_workspace_configurations = UpdateWorkspace(
            workspaceId=workspace_id,
            name=workspace_name,
            notifications=[Notification(slackConfiguration=SlackConfiguration())],
        )
        response = requests.post(
            url=f"{airbyte_host_url}{update_workspace_api}",
            data=update_workspace_configurations.json(
                exclude_defaults=False, exclude_unset=False, by_alias=True
            ),
            headers=headers,
        )
        response.raise_for_status()
        json_response = response.json()
        workspace_id = json_response["workspaceId"]
        logger.info(f"Workspace {workspace_name} updated : True")
        return workspace_id
    else:
        response.raise_for_status()
