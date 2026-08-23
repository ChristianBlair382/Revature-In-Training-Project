# PYTHON-BASED

from typing import ClassVar
from datetime import datetime

class Diagnostic_Report:
    registry: ClassVar[list["Diagnostic_Report"]] = []

    def __init__(self, id: int, service_call_id: str, file_url: str, notes: str | None = None, created_at: datetime | None = None):
        self.id = id
        self.service_call_id = service_call_id
        self.file_url = file_url
        self.notes = notes
        self.created_at = created_at
        Diagnostic_Report.registry.append(self)

    def __repr__(self) -> str:
        return(f"Diagnostic Report(ID={self.id}, Service Call ID={self.service_call_id} File URL={self.file_url!r}, DateTime={self.created_at})")

    @classmethod
    def find_by_id(cls, id: int) -> "Diagnostic_Report | None":
        for diagnostic_report in cls.registry:
            if diagnostic_report.id == id:
                return diagnostic_report
        return None