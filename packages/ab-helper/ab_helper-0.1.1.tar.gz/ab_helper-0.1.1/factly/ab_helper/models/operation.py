from pydantic import BaseModel


# Operations
class Normalization(BaseModel):
    option: str = "basic"


class OperatorConfiguration(BaseModel):
    operatorType: str = "normalization"
    normalization: Normalization


class OperationCreate(BaseModel):
    workspaceId: str
    name: str
    operatorConfiguration: OperatorConfiguration
