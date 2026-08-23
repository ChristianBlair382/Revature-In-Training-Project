# PYTHON-BASED

from typing import ClassVar
from .enums import SERVICE_CALL_PRIORITY, SERVICE_CALL_STATUS

class Service_Call:
    registry: ClassVar[list["Service_Call"]] = []

    def __init__(self, id: int, title: str, atm_id: int, technician_id: int, priority: SERVICE_CALL_PRIORITY, status: SERVICE_CALL_STATUS = SERVICE_CALL_STATUS.PENDING):
        self.id = id
        self.title = title
        self.atm_id = atm_id
        self.technician_id = technician_id
        self.priority = priority
        self.status = status
        Service_Call.registry.append(self)

    def __repr__(self) -> str:
        return(f"Service Call(ID={self.id}, Title={self.title!r}, Status={self.status.value!r})")

    @classmethod
    def find_by_id(cls, id: int) -> "Service_Call | None":
        for service_call in cls.registry:
            if service_call.id == id:
                return service_call
        return None

    def update_status(self, new_status: SERVICE_CALL_STATUS) -> None:
        #need to check that the provided value is a valid status against the enum
        if not isinstance(new_status, SERVICE_CALL_STATUS):
            raise TypeError(f"Expected SERVICE_CALL_STATUS enum, got {type(new_status).__name__}")

        #if the current and new status is the same, do nothing    
        if self.status == new_status:
            return
        
        self.status == new_status