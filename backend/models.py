# backend/models.py
from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('chw', 'admin', name='role_enum'), default='chw', nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    facility_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    county = db.Column(db.String(100), nullable=True)
    nhif_accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PatientCase(db.Model):
    __tablename__ = 'patient_cases'
    id = db.Column(db.Integer, primary_key=True)
    chw_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facilities.id'), nullable=True)
    sex = db.Column(db.String(10), nullable=True)
    age_months = db.Column(db.Integer, nullable=True)
    symptoms = db.Column(db.JSON, nullable=True)
    vitals = db.Column(db.JSON, nullable=True)
    triage_result = db.Column(db.String(50), nullable=True)
    risk_score = db.Column(db.Float, nullable=True)
    referral_note = db.Column(db.JSON, nullable=True)
    synced = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
