from App.database import db

class ImageFeed(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sender =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reciever =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    distributor = db.Column(db.Integer, db.ForeignKey('distributor.id'), nullable=True)
    rating =  db.Column(db.Integer, db.ForeignKey('rating.id'), default = None, nullable=True)
    
    def __init__(self, sender, reciever, distributor):
        self.sender = sender
        self.reciever = reciever
        self.distributor = distributor

    def toJSON(self):
        return{
            'id': self.id,
            'sender': self.sender,
            'reciever': self.reciever,
            'distributor': self.distributor,
            'rating' :self.rating
        }