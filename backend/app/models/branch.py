from typing import ClassVar

class Branch:
    registry: ClassVar[list["Branch"]] = []

    def __init__(self, id: int, name: str, location_region: str, capacity: int, supervisor_id: int):
        self.id = id
        self.name = name
        self.location_region = location_region
        self.capacity = capacity
        self.supervisor_id = supervisor_id
        Branch.registry.append(self)

    def __repr__(self) -> str:
        return(f"Branch(ID={self.id}, Name={self.name!r}, Location Region={self.location_region})")

    @classmethod
    def find_by_id(cls, id: int) -> "Branch | None":
        for branch in cls.registry:
            if branch.id == id:
                return branch
        return None