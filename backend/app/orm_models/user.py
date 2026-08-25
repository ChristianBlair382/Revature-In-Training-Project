from __future__ import annotations

from sqlalchemy import Boolean, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums import ROLE

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    # Raw password is stored elsewhere; store hashed password instead
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[ROLE] = mapped_column(
        SqlEnum(
            ROLE,
            name="user_role",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=ROLE.AUDITOR,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
            return (f"User(ID={self.id}, Username={self.username!r}, Role={self.role.value})")