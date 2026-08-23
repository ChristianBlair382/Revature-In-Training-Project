# OMR-BASED

from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING 

from sqlalchemy import ForeignKey, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .service_call import Service_Call

class Diagnostic_Report(Base):
    __tablename__ = "diagnostic_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_call_id: Mapped[int] = mapped_column(Integer, ForeignKey("service_calls.id"))
    file_url: Mapped[str] = mapped_column(Text)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    # server_default=func.now() - defaults created_at to the current timestamp upon insertion
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    service_call: Mapped["Service_Call"] = relationship(back_populates="diagnostic_reports")

    def __repr__(self) -> str:
        return (f"Diagnostic Report(ID={self.id}, Service_Call ID={self.service_call_id!r}, File URL={self.file_url!r}, Created At: {self.created_at})")