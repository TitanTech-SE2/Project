from App.database import db

class ImageFeed(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reciever =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seen = db.Column(db.Boolean, default=False)
    distributorID = db.Column(db.Integer, db.ForeignKey('distributor.id'), nullable=True)
    
    def __init__(self, sender, reciever, distributer):
        self.sender = sender
        self.reciever = reciever
        self.distributorID = distributorID

    def toJSON(self):
        return{
            'id': self.id,
            'sender': self.sender,
            'reciever': self.reciever,
            'distributorID': self.distributorID,
        }