from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


#  ========USER Models=======

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(120), nullable = False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



# ================ PRODUCT MODEL ================

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)  # Men / Women / Unisex / Kids
    description = db.Column(db.Text)

    images = db.Column(db.Text, nullable=False)

    # Pricing
    selling_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)

    # Reviews
    average_rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "gender": self.gender,
            "description": self.description,
            "images": self.images.split(","),
            "selling_price": self.selling_price,
            "discount": self.discount,
            "average_rating": self.average_rating,
            "total_reviews": self.total_reviews,
        }