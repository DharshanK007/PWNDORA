from enum import Enum

class ClueType(str, Enum):
    TICKET = "Ticket"
    NOTE = "Employee Note"
    CONFIG = "Configuration"
    BACKUP = "Backup"
    FIRMWARE = "Firmware"
    EMAIL = "Email"
    DOCUMENTATION = "Documentation"
    AUDIT_LOG = "Audit Log"
    NETWORK_DIAGRAM = "Network Diagram"
    API_RESPONSE = "API Response"
