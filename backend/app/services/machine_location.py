from app.models.machine_location import MachineLocation
from app.schemas.machine_location import MachineLocationCreate, MachineLocationUpdate
from app.services.base import CRUDBase

class CRUDMachineLocation(CRUDBase[MachineLocation, MachineLocationCreate, MachineLocationUpdate]):
    pass

machine_location = CRUDMachineLocation(MachineLocation)
