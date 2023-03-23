import os
import unittest
import json

from app import create_app
from models import Actor, Movie

from dotenv import load_dotenv


class FinalTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        
        load_dotenv(dotenv_path='db_info.env')
        self.database_name = os.getenv('DATABASE_TEST_NAME')
        self.database_user = os.getenv('DATABASE_USER')
        self.database_password = os.getenv('DATABASE_PASSWORD')
        self.database_host = os.getenv('DATABASE_HOST')
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"
    
        return self.app

    def tearDown(self):
        pass

    '''
    Currently all successful endpoint tests are done.
    TODO: One test for error behavior of each endpoint
    TODO: At least two tests of RBAC for each role
    '''

    def test_index(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
    
    def test_get_actors_success(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['number_actors'], len(Actor.query.all()))
    
    def test_get_movies_success(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['number_movies'], len(Movie.query.all()))
    



# Make the tests conveniently executable 
if __name__ == "__main__":
    unittest.main()