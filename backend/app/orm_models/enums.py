from enum import Enum

class ATM_STATUS(str, Enum):
    OPERATIONAL = "Operational"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"

class SERVICE_CALL_STATUS(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In-Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

class SERVICE_CALL_PRIORITY(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    CRITICAL = "Critical"

class ROLE(str, Enum):
    OPERATIONS_ADMIN = "Operations_Admin"
    FIELD_TECHNICIAN = "Field_Technician"
    AUDITOR = "Auditor"