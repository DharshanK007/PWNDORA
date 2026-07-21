from app.events.base_event import BaseEvent

# Employee Events
class EmployeeActivated(BaseEvent): pass
class EmployeeTerminated(BaseEvent): pass

# Device Events
class DeviceRegistered(BaseEvent): pass
class DeviceConfigured(BaseEvent): pass
class DeviceActivated(BaseEvent): pass
class DeviceDecommissioned(BaseEvent): pass

# Firmware Events
class FirmwareSubmitted(BaseEvent): pass
class FirmwareApproved(BaseEvent): pass
class FirmwareDeployed(BaseEvent): pass
class FirmwareRollback(BaseEvent): pass

# Ticket Events
class TicketCreated(BaseEvent): pass
class TicketAssigned(BaseEvent): pass
class TicketStarted(BaseEvent): pass
class TicketResolved(BaseEvent): pass
class TicketClosed(BaseEvent): pass

# Inventory Events
class InventoryAllocated(BaseEvent): pass
class InventoryConsumed(BaseEvent): pass

# Report Events
class ReportPublished(BaseEvent): pass
class ReportArchived(BaseEvent): pass

# Auth Events
class LoginEvent(BaseEvent): pass
class FailedLoginEvent(BaseEvent): pass
class LogoutEvent(BaseEvent): pass
