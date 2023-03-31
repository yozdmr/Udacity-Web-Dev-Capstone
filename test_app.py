import os
import unittest
import json
from datetime import datetime

from app import create_app
from models import Actor, Movie

from dotenv import load_dotenv
from jose import jwt


class FinalTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        
        load_dotenv(dotenv_path='dbinfo.env')
        self.database_name = os.getenv('DATABASE_TEST_NAME')
        self.database_user = os.getenv('DATABASE_USER')
        self.database_password = os.getenv('DATABASE_PASSWORD')
        self.database_host = os.getenv('DATABASE_HOST')
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"
    
        # Enter valid token
        self.TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBDb09HYnU3TGJveThoTzhGRXhHdyJ9.eyJpc3MiOiJodHRwczovL3lvemRtci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjNkNmZmY2FiNDk1NjQwYThmMmNhYzEzIiwiYXVkIjoiZmluYWwiLCJpYXQiOjE2ODAyMjY2NDcsImV4cCI6MTY4MDIzMzg0NywiYXpwIjoiN0VqazFsdEU4amtsekhJR0JEQWpNZlVKV0JvUk5PdVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvciIsImdldDptb3ZpZSIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.FxhA8hTXL2LsG-JgryK3hHkE6QU6maTG-Fud8nIYjP5X-tEba8N3bhE0pzxgalyLT4wg_OQC_wWTfI2eA6N8jYK4Wi1VDOPZ7c4q-2YShkFxcx9wYcSVYza5oqkeyx7bfG0xUZ3Sxj1E_UqCqBkSkUxxlNBwu98idb0oCkiRIxzRMHffBJ2vDHzeBiK9Tdy4Pd7DWe63r1D9vdndFHXVvihbw_GFTe_H930CfQag5_qe0SCWK9k7bhz0_pleYTI19cdOfhMhCGWK4FfSHYdvJV50Pqt45QNU-B0uwhC2HX4fsf6fiQtUpXLEbGo6GfddvqcaCzv-znFcl_W5RaORSw'
        # set the authorization header with the token
        self.HEADERS = {'Authorization': f'Bearer {self.TOKEN}'}

    def tearDown(self):
        pass

    '''
    Requirements: 
     * One test for success behavior of each endpoint (DONE)
     * One test for error behavior of each endpoint (DONE)
     * At least two tests of RBAC for each role TODO
    '''

    # ---------------
    # TESTING INDEX
    # ---------------

    # Success
    def test_index(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    # Failure
    def test_index_bad_method(self):
        # Incorrect method
        res = self.client().post('/')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')
    
    
    
    # ---------------
    # TESTING ACTORS
    # ---------------

    # Get Success
    def test_get_actors_success(self):
        res = self.client().get('/actors', headers=self.HEADERS)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['number_actors'], len(Actor.query.all()))
    
    # Get Failure
    def test_get_actors_bad_method(self):
        res = self.client().delete('/actors', headers=self.HEADERS)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')
    
    # Post Success
    def test_post_actors_success(self):
        new_actor = {
            'name': 'John Doe',
            'age': 35,
            'gender': 'male'
        }
        res = self.client().post('/actors', headers=self.HEADERS, json=new_actor)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added_actor']['name'], 'John Doe')
        self.assertEqual(data['added_actor']['age'], 35)
        self.assertEqual(data['added_actor']['gender'], 'male')
    
    # Post Failure
    def test_post_actors_bad_data(self):
        new_actor = {
            'name': 'John Doe',
            'age': 35
        }
        res = self.client().post('/actors', headers=self.HEADERS, json=new_actor)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # Patch Success
    def test_patch_actors_success(self):
        actor = Actor(name='Test Actor', age=30, gender='Male')
        Actor.insert(actor)

        res = self.client().patch(f'/actors/{actor.id}', headers=self.HEADERS, json={'name': 'Modified Actor'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    # Patch Failure
    def test_patch_actors_bad_request(self):
        res = self.client().patch(f'/actors/999', headers=self.HEADERS, json={'name': 'Modified Actor'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')

    # Delete Success
    def test_delete_actors_success(self):
        actor = Actor(name='Test Actor', age=30, gender='Male')
        Actor.insert(actor)

        res = self.client().delete(f'/actors/{actor.id}', headers=self.HEADERS)
        data = json.loads(res.data)

        actor = Actor.query.get(actor.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(actor, None)

    # Delete Failure
    def test_delete_actors_bad_request(self):
        res = self.client().delete(f'/actors/999', headers=self.HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')
    


    # ---------------
    # TESTING MOVIES
    # ---------------

    # Success
    def test_get_movies_success(self):
        res = self.client().get('/movies', headers=self.HEADERS)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['number_movies'], len(Movie.query.all()))
    
    # Failure
    def test_get_movies_bad_method(self):
        res = self.client().delete('/movies', headers=self.HEADERS)
        data = json.loads(res.data)
        
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')
    
    # Post Success
    def test_post_movies_success(self):
        sample_date = datetime.now()

        new_movie = {
            'title': 'Good Movie',
            'release_date': sample_date
        }
        res = self.client().post('/movies', headers=self.HEADERS, json=new_movie)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added_movie']['title'], 'Good Movie')
    
    # Post Failure
    def test_post_movies_bad_data(self):
        new_movie = {
            'title': 'Good Movie'
        }
        res = self.client().post('/movies', headers=self.HEADERS, json=new_movie)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # Patch Success
    def test_patch_movies_success(self):
        sample_date = datetime.now()
        movie = Movie(title='Test Movie', release_date=sample_date)
        Movie.insert(movie)

        res = self.client().patch(f'/movies/{movie.id}', headers=self.HEADERS, json={'title': 'Modified Movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Patch Failure
    def test_patch_movies_bad_request(self):
        res = self.client().patch(f'/movies/999', headers=self.HEADERS, json={'name': 'Modified Movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')

    # Delete Success
    def test_delete_movies_success(self):
        sample_date = datetime.now()
        movie = Movie(title='Test Movie', release_date=sample_date)
        Movie.insert(movie)

        res = self.client().delete(f'/movies/{movie.id}', headers=self.HEADERS)
        data = json.loads(res.data)

        movie = Movie.query.get(movie.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(movie, None)
    
    # Delete Failure
    def test_delete_movies_bad_request(self):
        res = self.client().delete(f'/movies/999', headers=self.HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')
    


    # TODO: RBAC Tests --------



# Make the tests conveniently executable 
if __name__ == "__main__":
    unittest.main()