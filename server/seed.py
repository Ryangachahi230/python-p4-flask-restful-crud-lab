#!/usr/bin/env python3
from app import app
from models import db, Plant
from datetime import datetime, timedelta

with app.app_context():
    # Recreate tables (fine for local labs)
    db.drop_all()
    db.create_all()

    # Only seed if empty
    if not Plant.query.first():
        plants = [
            Plant(name="Aloe", image="./images/aloe.jpg", price=11.50),
            Plant(name="ZZ Plant", image="./images/zz-plant.jpg", price=25.98, is_in_stock=False),
            Plant(name="Peace Lily", image="./images/peace-lily.jpg", price=15.99),
            Plant(name="Fiddle Leaf Fig", image="./images/fiddle-leaf.jpg", price=45.00),
            Plant(name="Snake Plant", image="./images/snake-plant.jpg", price=18.25),
        ]

        try:
            db.session.add_all(plants)
            db.session.commit()
            print("✅ Database seeded successfully with", len(plants), "plants.")
        except Exception as e:
            db.session.rollback()
            print("❌ Error seeding database:", e)
    else:
        print("⚠️ Database already contains data. Skipping seeding.")
