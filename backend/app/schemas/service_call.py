from pydantic import BaseModel, ConfigDict, Field

from app.orm_models.enums import SERVICE_CALL_STATUS, SERVICE_CALL_PRIORITY

class Service_Call_Base(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    atm_id: int
    technician_id: int
    priority: SERVICE_CALL_PRIORITY = SERVICE_CALL_PRIORITY.MEDIUM
    status: SERVICE_CALL_STATUS = SERVICE_CALL_STATUS.PENDING

class Service_Call_Create(Service_Call_Base):
    """"""

class Service_Call_Read(Service_Call_Base):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Discrepency_Read(BaseModel):
    service_call_id: int
    title: str = Field(min_length=1, max_length=100)
    atm_id: int
    technician_id: int
    atm_branch_id: int
    technician_branch_id: int
    model_config = ConfigDict(from_attributes=True)