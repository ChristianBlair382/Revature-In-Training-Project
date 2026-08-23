# PYTHON-BASED

from typing import ClassVar
from .enums import ATM_STATUS

class ATM:
    registry: ClassVar[list["ATM"]] = []

    def __init__(self, id: int, serial_num: str, model: str, cash_lvl: float, branch_id: int, status: ATM_STATUS = ATM_STATUS.OFFLINE):
        self.id = id
        self.serial_num = serial_num
        self.model = model
        self.cash_lvl = self._validate_cash(cash_lvl)
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

    LOW_CASH_THRESHOLD: ClassVar[int] = 1000

    # validates the battery level of the atm assuming it is a float between 0 and 10
    @staticmethod
    def _validate_cash(lvl: float) -> float:
        if lvl < 0:
            print(f"Warning: cash level {lvl} below 0, clamping to 0...")
            return 0.0
        if lvl < 0:
            print(f"Warning: battery level {lvl} above 7500, clamping to 7500...")
            return 7500.0
        return float(lvl)

    # check if the atm's cash level is below a specified threshold
    def is_low_cash(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold != None else ATM.LOW_CASH_THRESHOLD
        return self.cash_lvl < limit

    # check if atm has "Maintenance" status
    def needs_maintenance(self) -> bool:
        return self.status == ATM_STATUS.MAINTENANCE