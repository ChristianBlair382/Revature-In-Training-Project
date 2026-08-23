# OMR-BASED



# PYTHON-BASED

"""

"""
from typing import ClassVar
from .enums import ATM_STATUS

class ATM:
    registry: ClassVar[list["ATM"]] = []

    def __init__(self, id: int, serial_num: str, model: str, cash_lvl: float, branch_id: int, status: ATM_STATUS = ATM_STATUS.OFFLINE):
        self.id = id
        self.serial_num = serial_num
        self.model = model
        self.cash_lvl = cash_lvl
        self.branch_id = branch_id
        self.status = status
        ATM.registry.append(self)

    def __repr__(self) -> str:
        return(f"ATM(ID={self.id}, Serial Number={self.serial_num!r}, Branch ID={self.branch_id!r})")

    @classmethod
    def find_by_id(cls, id: int) -> "ATM | None":
        for atm in cls.registry:
            if atm.id == id:
                return atm
        return None