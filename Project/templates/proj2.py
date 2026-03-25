from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    olid = db.Column(db.String(64), unique=True, nullable=True) 
    title = db.Column(db.String(512), nullable=False)
    authors = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(64), nullable=True)
    license = db.Column(db.String(128), default="All rights reserved")
    filename = db.Column(db.String(256), nullable=True)  
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    borrowed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    borrowed_until = db.Column(db.DateTime, nullable=True)

    @property
    def is_borrowed(self):
        return self.borrowed_by_id 