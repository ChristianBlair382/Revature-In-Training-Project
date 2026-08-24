from pydantic import BaseModel, ConfigDict, Field

class Branch_Base(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location_region: str = Field(min_length=1, max_length=50)
    capacity: int
    supervisor_id: int

class Branch_Create(Branch_Base):
    """"""

class Branch_Read(Branch_Base):
    id: int
    model_config = ConfigDict(from_attributes=True)