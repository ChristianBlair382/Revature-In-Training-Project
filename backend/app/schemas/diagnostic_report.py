from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class Diagnostic_Report_Base(BaseModel):
    service_call_id: int
    file_url: str = Field(min_length=1)
    notes: str | None = None

class Diagnostic_Report_Create(Diagnostic_Report_Base):
    """"""

class Diagnostic_Report_Read(Diagnostic_Report_Base):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)