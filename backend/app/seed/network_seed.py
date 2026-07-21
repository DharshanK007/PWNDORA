from app.models.network import NetworkZone, NetworkLink

def seed_networks(db):
    zone_names = ["Corporate LAN", "DMZ", "Factory LAN", "OT Network", "ICS Zone", "PLC Network", "VPN"]
    zones = {}
    for idx, name in enumerate(zone_names):
        z = db.query(NetworkZone).filter(NetworkZone.name == name).first()
        if not z:
            z = NetworkZone(name=name, vlan_id=10+idx, subnet=f"10.0.{idx}.0/24", trust_level="Medium", routing_direction="Bi-directional")
            db.add(z)
            db.flush()
        zones[name] = z
    db.commit()
    
    # Create links if not exist
    if db.query(NetworkLink).count() == 0:
        links = [
            ("Corporate LAN", "DMZ"),
            ("DMZ", "Factory LAN"),
            ("Factory LAN", "OT Network"),
            ("OT Network", "ICS Zone"),
            ("ICS Zone", "PLC Network")
        ]
        for src, dst in links:
            if src in zones and dst in zones:
                link = NetworkLink(
                    source_zone_id=zones[src].id,
                    target_zone_id=zones[dst].id,
                    description=f"Route from {src} to {dst}"
                )
                db.add(link)
        db.commit()
    print("Seeded Network Zones and Links")
