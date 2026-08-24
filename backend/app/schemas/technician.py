from pydantic import BaseModel, ConfigDict, Field

class Technician_Base(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    branch_id: int

class Technician_Create(Technician_Base):
    """"""

class Technician_Read(Technician_Base):
    id: int
    model_config = ConfigDict(from_attributes=True)