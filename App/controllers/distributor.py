from App.models import User, Distributor, ImageFeed
from App.controllers import user, imageFeed
from App.database import db
from .user import (get_all_users, get_user)
import random, datetime

def createNewDistributor(users):
    distributor = Distributor(users)
    db.session.add(distributor)
    db.session.commit()
    return distributor

def GenerateFeed(sender):
    users = get_all_users()
    boolVar=False
    if users:
        usersNum = len(users)   
        current = usersNum
        current2 = current - 1
        dump= []    
        while len(dump) < current2:          
            randomNumber = random.randint(1, usersNum)
            randomUser = get_user(randomNumber)
            haul=[]
            for x in haul:
                if(x==randomUser):
                   boolVar=True
            if(boolVar==False):  
                haul.append(randomUser)
                if randomNumber != sender:
                    dump.append(randomUser)               
                    new=createNewDistributor(current2)
                    neww=createImageFeed(sender, randomNumber,new.distributeId)
        
        return dump
         
    return None