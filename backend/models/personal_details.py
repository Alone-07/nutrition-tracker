import uuid
from app import db
from sqlalchemy.dialects.mysql import CHAR

class PersonalDetails(db.Model):
    __tablename__ = 'personal_details'

    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(CHAR(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    weight = db.Column(db.Float, nullable=True)     # in kilograms
    height = db.Column(db.Float, nullable=True)     # in centimeters
    gender = db.Column(db.Enum('Male', 'Female', 'Others'), nullable=True)

    # Establish relationship back to User
    user = db.relationship('User', backref=db.backref('personal_details', uselist=False, cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<PersonalDetails {self.id} - {self.user_id}>"
