import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
from datetime import date, datetime

from App.main import create_app
from App.database import create_db
from App.models import User, Image, Rating, Ranking, ImageFeed, Distributor
from App.controllers import (
    create_user,
    get_user,
    get_user_by_username,
    get_all_users,
    get_all_users_json,
    update_user,
    delete_user,

    create_image,
    get_all_images,
    get_all_images_json,
    get_images_by_userid_json,
    get_image,
    get_image_json,
    delete_image,

    create_rating, 
    get_all_ratings,
    get_all_ratings_json,
    get_rating,
    get_ratings_by_target,
    get_ratings_by_creator,
    get_rating_by_actors,
    update_rating,
    get_calculated_rating,
    get_level,

    create_ranking, 
    get_all_rankings,
    get_all_rankings_json,
    get_ranking,
    get_rankings_by_image,
    get_rankings_by_creator,
    get_ranking_by_actors,
    get_calculated_ranking,
    update_ranking,
    createImageFeed,
    getImageFeed,
    createNewDistributor,
    GenerateFeed,
    authenticate
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_toJSON(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "images": [], "ratings": []})
    
    def test_hashed_password(self):
        password = "mypassword"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class DistributorUnitTests(unittest.TestCase):
    def test_new_dist(self):
        dist = Distributor(3)
        assert dist.numberProfiles == 3

    def test_to_json(self):
        dist = Distributor(3)
        self.assertDictEqual(dist.toJSON(),{'id': None, 'time': None, 'numberProfiles': 3})

class ImageFeedUnitTests(unittest.TestCase):
    def test_new_imageFeed(self):
        new_imageFeed = ImageFeed(1,1,2)
        assert new_imageFeed.id == None

    def test_new_imageFeed_toJSON(self):
        new_imageFeed = ImageFeed(1,1,2)
        new_imageFeed_toJSON = new_imageFeed.toJSON()
        self.assertDictEqual(new_imageFeed_toJSON, {'id': None, 'sender': 1, 'reciever': 1, 'distributor': 2, 'rating': None})

class ImageUnitTests(unittest.TestCase):

    def test_new_image(self):
        image = Image(1, "testImage")
        assert image.rankings == []

    def test_toJSON(self):
        image = Image(1, "testImage")
        image_json = image.toJSON()
        self.assertDictEqual(image_json, {'id': None, 'user': 1, 'rankings': [], 'url': 'testImage'})

class RatingUnitTests(unittest.TestCase):

    def test_new_rating(self):
        rating = Rating(1, 2, 3)
        assert rating.score == 3

    def test_toJSON(self):
        rating = Rating(1, 2, 3)
        rating_json = rating.toJSON()
        self.assertDictEqual(rating_json, {"id":None, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()})

class RankingUnitTests(unittest.TestCase):

    def test_new_ranking(self):
        ranking = Ranking(1, 2, 3)
        assert ranking.score == 3

    def test_toJSON(self):
        ranking = Ranking(1, 2, 3)
        ranking_json = ranking.toJSON()
        self.assertDictEqual(ranking_json, {"id":None, "creatorId":1, "imageId": 2, "score":3})

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

def test_authenticate():
        user = create_user("bob", "bobpass")
        assert authenticate("bob", "bobpass") != None


class UsersIntegrationTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_toJSON(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "images": [], "ratings": []})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

    def test_toJSON(self):
        image = Image(1)
        image_json = image.toJSON()
        self.assertDictEqual(image_json, {"id":None, "rankings":[], "user": 1})

    def test_new_rating(self):
        rating = Rating(1, 2, 3)
        assert rating.score == 3

    def test_toJSON(self):
        rating = Rating(1, 2, 3)
        rating_json = rating.toJSON()
        self.assertDictEqual(rating_json, {"id":None, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()})

    def test_new_ranking(self):
        ranking = Ranking(1, 2, 3)
        assert ranking.score == 3

    def test_toJSON(self):
        ranking = Ranking(1, 2, 3)
        ranking_json = ranking.toJSON()
        self.assertDictEqual(ranking_json, {"id":None, "creatorId":1, "imageId": 2, "score":3})

class ImageIntegrationTests(unittest.TestCase):

    def test_create_image(self):
        image = create_image(2, "testImage")
        assert image.id == 1

    def test_get_image(self):
        image = get_image(1)
        assert image.user == 2

    def test_get_all_images(self):
        image = create_image(1, "testImage")
        imageList = []
        imageList.append(get_image(1))
        imageList.append(get_image(2))
        self.assertListEqual(get_all_images(), imageList)

    def test_get_all_images_json(self):
        images_json = get_all_images_json()
        self.assertListEqual([{'id': 1, 'rankings': [], 'url': 'testImage', 'user': 2},{'id': 2, 'rankings': [], 'url': 'testImage', 'user': 1}], images_json)

    def test_get_images_by_userid_json(self):
        images_json = get_images_by_userid_json(2)
        self.assertListEqual(images_json, [{'id': 1, 'user': 2, 'rankings': [], 'url': 'testImage'}])

    def test_delete_image(self):
        image = create_image(1, "testImage")
        delete_image(image.id)
        image = get_image(image.id)
        assert image == None

class DistributorIntegrationTests(unittest.TestCase):
    def test_create_new_distributor(self):
        dist = createNewDistributor(6)
        assert dist != None

    def test_new_feed_generation(self):
        dist = GenerateFeed(1)
        assert dist != None

class ImageFeedIntegrationTests(unittest.TestCase):
    def test_create_imageFeed(self):
        imageFeed = createImageFeed(1,2,3)
        assert imageFeed.sender == 1

    def test_get_imageFeed(self):
        imageFeed = getImageFeed(2)
        self.assertListEqual(imageFeed, [{'id': 1, 'sender': 1, 'reciever': 2, 'distributor': 3, 'rating': None}])

class RatingIntegrationTests(unittest.TestCase):

    def test_create_rating(self):
        rating = create_rating(1, 2, 3)
        assert rating.id == 1

    def test_get_rating(self):
        rating = get_rating(1)
        assert rating.creatorId == 1

    def test_get_all_ratings(self):
        rating = create_rating(2, 1, 4)
        ratingList = []
        ratingList.append(get_rating(1))
        ratingList.append(get_rating(2))
        self.assertListEqual(get_all_ratings(), ratingList)

    def test_get_all_ratings_json(self):
        ratings_json = get_all_ratings_json()
        self.assertListEqual([{"id":1, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()}, {"id":2, "creatorId":2, "targetId": 1, "score":4, "timeStamp": date.today()}], ratings_json)

    def test_get_ratings_by_creatorid(self):
        ratings = get_ratings_by_creator(2)
        self.assertListEqual(ratings, [{"id":2, "creatorId":2, "targetId": 1, "score":4, "timeStamp": date.today()}])

    def test_get_ratings_by_targetid(self):
        ratings = get_ratings_by_target(2)
        self.assertListEqual(ratings, [{"id":1, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()}])

    def test_update_rating(self):
        rating = update_rating(1, 5)
        assert rating.score == 5

    def test_try_calculate_rating(self):
        user = create_user("phil", "philpass")
        rating = create_rating(user.id, 2, 5)
        calculated = get_calculated_rating(2)
        assert calculated == 4

    def test_get_level(self):
        assert get_level(1) == 1


class RankingIntegrationTests(unittest.TestCase):

    def test_create_rating(self):
        ranking = create_ranking(1, 2, 3)
        assert ranking.id == 1

    def test_get_ranking(self):
        ranking = get_ranking(1)
        assert ranking.creatorId == 1

    def test_get_all_rankings(self):
        ranking = create_ranking(2, 1, 4)
        rankingList = []
        rankingList.append(get_ranking(1))
        rankingList.append(get_ranking(2))
        self.assertListEqual(get_all_rankings(), rankingList)

    def test_get_all_rankings_json(self):
        rankings_json = get_all_rankings_json()
        self.assertListEqual([{"id":1, "creatorId":1, "imageId": 2, "score":3}, {"id":2, "creatorId":2, "imageId": 1, "score":4}], rankings_json)

    def test_get_rankings_by_creatorid(self):
        rankings = get_rankings_by_creator(2)
        self.assertListEqual(rankings, [{"id":2, "creatorId":2, "imageId": 1, "score":4}])

    def test_get_rankings_by_imageid(self):
        rankings = get_rankings_by_image(2)
        self.assertListEqual(rankings, [{"id":1, "creatorId":1, "imageId": 2, "score":3}])

    def test_get_ranking_by_actors(self):
        ranking = get_ranking_by_actors(1, 2)
        assert ranking.id == 1

    def test_update_ranking(self):
        ranking = update_ranking(1, 5)
        assert ranking.score == 5

    def test_try_calculate_ranking(self):
        ranking = create_ranking(3, 2, 5)
        calculated = get_calculated_ranking(2)
        assert calculated == 4