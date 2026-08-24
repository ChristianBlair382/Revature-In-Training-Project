from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

from app.orm_models.enums import ATM_STATUS

class ATM_Base(BaseModel):
    serial_num: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)
    cash_lvl: Decimal = Field(ge=0, le=7500)
    branch_id: int
    status: ATM_STATUS = ATM_STATUS.OFFLINE

class ATM_Create(ATM_Base):
    """"""

class ATM_Read(ATM_Base):
    id: int
    model_config = ConfigDict(from_attributes=True)