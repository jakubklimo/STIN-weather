from ..service.database import db

class Location(db.Model):
    id = db.Column("location_id", db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    def __init__(self, location, user):
        self.location = location
        self.user = user

