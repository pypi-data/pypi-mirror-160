import json
import logging
import logging.config
from typing import Any, Dict

import requests

from .core.configs import Settings

settings = Settings()

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def check_health(airbyte_host_url: str, health_check_api: str, headers: Dict[str, Any]):
    response = requests.get(
        url=f"{airbyte_host_url}{health_check_api}",
        headers=headers,
    )
    response.raise_for_status()

    json_response = response.json()
    if not json_response["available"]:
        logger.error(f"Server {airbyte_host_url} status : ILL")
        raise requests.ConnectionError
    logger.info(f"Server {airbyte_host_url} status : HEALTHY")
    return True


def find_workspace_id_by_slug(
    airbyte_host_api, find_workspace_by_slug_api, workspace_name, headers
):
    # find if the required workspace exist or not
    response = requests.post(
        url=f"{airbyte_host_api}{find_workspace_by_slug_api}",
        data=json.dumps({"slug": workspace_name}),
        headers=headers,
    )
    response.raise_for_status()
    json_response = response.json()
    workspace_id = json_response["workspaceId"]
    logger.info(f"Workspace {workspace_name} created with ID : {workspace_id}")
    return workspace_id
