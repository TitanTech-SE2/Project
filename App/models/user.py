from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask import jsonify
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String, nullable=True, unique=True)
    dateAdded = db.Column(db.DateTime, default = datetime.utcnow)
    images = db.relationship('Image', backref='image', lazy=True, cascade="all, delete-orphan")
    ratings = db.relationship('Rating', backref='rating', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username,
            'profile_pic': self.profile_pic,
            'images': [image.toJSON() for image in self.images],
            'ratings': [rating.toJSON() for rating in self.ratings],
            'dateAdded' : self.dateAdded
        }
    

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
