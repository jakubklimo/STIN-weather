from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from ..service.database import db

class User(db.Model):
    id = db.Column("user_id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200))
    premium_ex = db.Column(db.DateTime)
    locations = db.relationship("Location", backref="user", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_premium(self, duration_months):
        current_time = datetime.now()
        if self.premium_ex is not None and current_time < self.premium_ex:
            self.premium_ex += timedelta(days=30 * duration_months)
        else:
            self.premium_ex = current_time + timedelta(days=30 * duration_months)

    def is_subscriber(self):
        current_time = datetime.now()
        if self.premium_ex is not None and current_time < self.premium_ex:
            return True
        else:
            return False