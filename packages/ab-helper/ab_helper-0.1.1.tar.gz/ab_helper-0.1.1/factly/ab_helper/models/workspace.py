from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel


class SlackConfiguration(BaseModel):
    webhook: str = ""


class Notification(BaseModel):
    notificationType: str = "slack"
    sendOnSuccess: bool = False
    sendOnFailure: bool = False
    slackConfiguration: SlackConfiguration
    customerioConfiguration: Dict[str, Any] = {}


class CreateWorkspace(BaseModel):
    email: str = "techteam@factly.com"
    anonymousDataCollection: bool = False
    name: str
    news: bool = False
    securityUpdates: bool = False
    notifications: List[Notification]
    displaySetupWizard: bool = False


class UpdateWorkspace(BaseModel):
    workspaceId: str
    initialSetupComplete: bool = True
    email: str = "techteam@factly.com"
    anonymousDataCollection: bool = False
    news: bool = False
    securityUpdates: bool = False
    notifications: List[Notification]
    displaySetupWizard: bool = False
