# OMR-BASED

from __future__ import annotations
from typing import TYPE_CHECKING 

from sqlalchemy import ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import SERVICE_CALL_PRIORITY, SERVICE_CALL_STATUS

if TYPE_CHECKING:
    from .diagnostic_report import Diagnostic_Report
    from .technician import Technician
    from .atm import ATM

class Service_Call(Base):
    __tablename__ = "service_calls"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    atm_id: Mapped[int] = mapped_column(Integer, ForeignKey("atms.id"))
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("technicians.id"))
    priority: Mapped[SERVICE_CALL_PRIORITY] = mapped_column(
        SqlEnum(
            SERVICE_CALL_PRIORITY,
            name="service_call_priority",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=SERVICE_CALL_PRIORITY.MEDIUM
    )
    status: Mapped[SERVICE_CALL_STATUS] = mapped_column(
        SqlEnum(
            SERVICE_CALL_STATUS,
            name="service_call_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=SERVICE_CALL_STATUS.PENDING
    )

    atm: Mapped["ATM"] = relationship(back_populates="service_calls")
    technician: Mapped["Technician"] = relationship(back_populates="service_calls")
    # mapped lists are singular since they refer to one object having multiple linked objects via the list
    diagnostic_reports: Mapped[list["Diagnostic_Report"]] = relationship(back_populates="service_call") 

    def __repr__(self) -> str:
        return (f"Service_Call(ID={self.id}, Title={self.title!r}, Priority={self.priority!r}, Status={self.status.value})")

    def update_status(self, new_status: SERVICE_CALL_STATUS) -> None:
        #need to check that the provided value is a valid status against the enum
        if not isinstance(new_status, SERVICE_CALL_STATUS):
            raise TypeError(f"Expected MissionStatus enum, got {type(new_status).__name__}")

        #if the current and new status is the same, do nothing    
        if self.status == new_status:
            return
        
        self.status = new_status