# OMR-BASED

from __future__ import annotations 
from typing import TYPE_CHECKING 

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .branch import Branch
    from .service_call import Service_Call

class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id")) # foreign key setup

    branch: Mapped["Branch"] = relationship(back_populates="technicians")
    service_calls: Mapped[list["Service_Call"]] = relationship(back_populates="technician")

    def __repr__(self) -> str:
        return (f"Technician(ID={self.id}, Name={self.name!r}, Branch_ID={self.branch_id!r})")