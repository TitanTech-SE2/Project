from App.database import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rankings = db.relationship('Ranking', backref='ranking', lazy=True, cascade="all, delete-orphan")
    url = db.Column(db.String, nullable=False)

    def __init__(self, user, url):
        self.user = user
        self.url = url

    def toJSON(self):
        return{
            'id': self.id,
            'user': self.user,
            'rankings': [ranking.toJSON() for ranking in self.rankings],
            'url' : self.url 
        }