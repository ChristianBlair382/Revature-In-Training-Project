# OMR-BASED

from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING 

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import ATM_STATUS

if TYPE_CHECKING:
    from .branch import Branch
    from .service_call import Service_Call

class ATM(Base):
    __tablename__ = "atms"

    __table_args__ = (
        CheckConstraint(
            "cash_lvl BETWEEN 0 AND 10000",
            name="cash_level_range"
        ), # must be a tuple, so added a comma
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_num: Mapped[str] = mapped_column(String(50), unique=True)
    model: Mapped[str] = mapped_column(String(100))
    cash_lvl: Mapped[Decimal] = mapped_column(Numeric(6,2))
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("branches.id"))
    status: Mapped[ATM_STATUS] = mapped_column(
        SqlEnum(
            ATM_STATUS,
            name="atm_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=ATM_STATUS.OFFLINE,
    )

    branch: Mapped["Branch"] = relationship(back_populates="atms")
    service_calls: Mapped[list["Service_Call"]] = relationship(back_populates="atm")

    def __repr__(self) -> str:
        return (f"ATM(Serial={self.serial_num!r}, Model={self.model!r}, Cash=${self.cash_lvl}, Status={self.status.value})")
    
    LOW_CASH_THRESHOLD: int = 1000

    def is_low_cash(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else ATM.LOW_CASH_THRESHOLD
        return self.cash_lvl < limit

    def needs_maintenance(self) -> bool:
            return self.status == ATM_STATUS.MAINTENANCE