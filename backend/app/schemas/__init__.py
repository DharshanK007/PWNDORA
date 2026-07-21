from .base import PagedResponse
from .user import UserBase, UserCreate, UserUpdate, UserResponse
from .employee import EmployeeBase, EmployeeCreate, EmployeeUpdate, EmployeeResponse
from .department import DepartmentBase, DepartmentCreate, DepartmentUpdate, DepartmentResponse
from .device import DeviceBase, DeviceCreate, DeviceUpdate, DeviceResponse
from .firmware import FirmwareBase, FirmwareCreate, FirmwareUpdate, FirmwareResponse
from .machine_location import MachineLocationBase, MachineLocationCreate, MachineLocationUpdate, MachineLocationResponse
from .maintenance_ticket import MaintenanceTicketBase, MaintenanceTicketCreate, MaintenanceTicketUpdate, MaintenanceTicketResponse
from .inventory import InventoryBase, InventoryCreate, InventoryUpdate, InventoryResponse
from .notification import NotificationCreate, NotificationUpdate, NotificationResponse
from .report import ReportBase, ReportCreate, ReportUpdate, ReportResponse
from .activity_log import ActivityLogBase, ActivityLogCreate, ActivityLogResponse
