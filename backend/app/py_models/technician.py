# PYTHON-BASED

from typing import ClassVar

class Technician:
    registry: ClassVar[list["Technician"]] = []

    def __init__(self, id: int, name: str, branch_id: int):
        self.id = id
        self.name = name
        self.branch_id = branch_id
        Technician.registry.append(self)

    def __repr__(self) -> str:
        return(f"Technician(ID={self.id}, Name={self.name!r}, Branch ID={self.branch_id})")

    @classmethod
    def find_by_id(cls, id: int) -> "Technician | None":
        for technician in cls.registry:
            if technician.id == id:
                return technician
        return None