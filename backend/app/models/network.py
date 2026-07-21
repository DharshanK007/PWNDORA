from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class NetworkZone(Base):
    __tablename__ = "network_zones"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    trust_level: Mapped[str] = mapped_column(String(50), nullable=True)
    routing_direction: Mapped[str] = mapped_column(String(50), nullable=True)

    vlan_id: Mapped[int] = mapped_column(Integer, nullable=True)
    subnet: Mapped[str] = mapped_column(String(50), nullable=True)

    devices: Mapped[list["Device"]] = relationship("Device", back_populates="network_zone", lazy="selectin")

from sqlalchemy import ForeignKey
class NetworkLink(Base):
    __tablename__ = "network_links"
    
    source_zone_id: Mapped[str] = mapped_column(String(36), ForeignKey("network_zones.id"), nullable=False)
    target_zone_id: Mapped[str] = mapped_column(String(36), ForeignKey("network_zones.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    trust_level: Mapped[str] = mapped_column(String(50), nullable=True)
    routing_direction: Mapped[str] = mapped_column(String(50), nullable=True)


    source_zone: Mapped["NetworkZone"] = relationship("NetworkZone", foreign_keys=[source_zone_id])
    target_zone: Mapped["NetworkZone"] = relationship("NetworkZone", foreign_keys=[target_zone_id])
