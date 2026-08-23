# OMR-BASED

from __future__ import annotations # python treats every annotation as a string literal
from typing import TYPE_CHECKING # indicates that certain imports are only needed for type checking and not at runtime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .technician import Technician
    from .atm import ATM

class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(50))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)

    # establishes the relationships between other tables; bypasses order of creation
    atms: Mapped[list["ATM"]] = relationship(back_populates="branch")
    technicians: Mapped[list["Technician"]] = relationship(back_populates="branch")

    def __repr__(self) -> str:
        return(f"Branch(ID={self.id}, Name={self.name!r}, Region={self.location_region!r})")