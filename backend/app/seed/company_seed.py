from app.models.company import CompanyProfile

def seed_company(db):
    company = db.query(CompanyProfile).first()
    if not company:
        company = CompanyProfile(
            name="NeoFactory Industries",
            description="Leading manufacturer of smart industrial components.",
            headquarters="Detroit, MI, USA",
            business_units=["Automotive", "Aerospace", "Consumer Electronics"],
            industry="Manufacturing",
            employee_count=15000,
            contact_email="contact@neofactory.com",
            business_domain="Industrial Automation",
            security_level="Tier-2 Enterprise",
            factory_count=5,
            office_count=12,
            critical_infrastructure_type="Smart Factory",
            timezone="UTC-5"
        )
        db.add(company)
        db.commit()
    print("Seeded Company Profile")
