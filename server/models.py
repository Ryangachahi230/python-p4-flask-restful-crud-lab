from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class Plant(db.Model):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('price')
    def validate_price(self, key, value):
        if value is None or value < 0:
            raise ValueError("Price must be a non-negative number.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": round(self.price, 2),
            "is_in_stock": self.is_in_stock,
        }

    def __repr__(self):
        return f"<Plant {self.id}: {self.name} | In Stock: {self.is_in_stock}>"
