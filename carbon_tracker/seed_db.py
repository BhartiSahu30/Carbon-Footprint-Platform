# seed_db.py
from app import app, db, CarbonLog

# Sample historical environmental footprint metrics over the past week
sample_history = [
    {"date": "2026-06-13", "transport": 25.5, "energy": 12.4, "diet": 2.5, "waste": 1.04},
    {"date": "2026-06-14", "transport": 34.0, "energy": 14.1, "diet": 3.3, "waste": 1.04},
    {"date": "2026-06-15", "transport": 10.2, "energy": 11.8, "diet": 1.4, "waste": 0.30},
    {"date": "2026-06-16", "transport": 0.0,  "energy": 9.5,  "diet": 0.9, "waste": 0.30},
    {"date": "2026-06-17", "transport": 15.3, "energy": 15.2, "diet": 2.5, "waste": 1.04},
    {"date": "2026-06-18", "transport": 20.4, "energy": 13.0, "diet": 2.5, "waste": 1.04},
    {"date": "2026-06-19", "transport": 5.1,  "energy": 7.1,  "diet": 1.4, "waste": 0.30}
]

with app.app_context():
    # Create the database file and tables if they don't exist yet
    db.create_all()
    
    # Check if data already exists to prevent duplicate injection
    if CarbonLog.query.first() is None:
        print("Empty ledger detected. Injecting baseline sustainability logs...")
        
        for record in sample_history:
            total = record["transport"] + record["energy"] + record["diet"] + record["waste"]
            log_entry = CarbonLog(
                timestamp=record["date"],
                transport_emissions=record["transport"],
                energy_emissions=record["energy"],
                diet_emissions=record["diet"],
                waste_emissions=record["waste"],
                total_daily=round(total, 2)
            )
            db.session.add(log_entry)
            
        db.session.commit()
        print("Database successfully built and seeded as 'instance/database.db'!")
    else:
        print("Database already contains records. Skipping seed process.")