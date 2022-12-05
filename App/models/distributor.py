from App.database import db
from datetime import datetime


class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)
    numberProfiles = db.Column(db.Integer, nullable=False)
    
    def __init__(self, numberProfiles):
        self.numberProfiles = numberProfiles


    def toJSON(self):
        return{
            'id': self.id,
            'time': self.time,
            'numberProfiles': self.numberProfiles      
        }