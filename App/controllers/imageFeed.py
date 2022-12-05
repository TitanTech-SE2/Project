
from App.models import ImageFeed
from App.controllers import distributor
from App.database import db


def createImageFeed(sender, reciever, distributor):
    imageFeed = ImageFeed(sender, reciever, distributor)
    db.session.add(imageFeed)
    db.session.commit()
    return imageFeed


def getImageFeed(reciever):
    imageFeed =  ImageFeed.query.filter_by(reciever=reciever)
    imageFeed = [image.toJSON() for image in imageFeed]    
    return imageFeed