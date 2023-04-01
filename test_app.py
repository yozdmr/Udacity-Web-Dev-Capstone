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
    
        # Enter Executive Producer token
        self.EXECUTIVE_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBDb09HYnU3TGJveThoTzhGRXhHdyJ9.eyJpc3MiOiJodHRwczovL3lvemRtci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjNkNmZmY2FiNDk1NjQwYThmMmNhYzEzIiwiYXVkIjoiZmluYWwiLCJpYXQiOjE2ODAzNjEwODQsImV4cCI6MTY4MDQ0NzQ4NCwiYXpwIjoiN0VqazFsdEU4amtsekhJR0JEQWpNZlVKV0JvUk5PdVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvciIsImdldDptb3ZpZSIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.Fp1viH_OeukkZwrICxqxvT3aHI1fPQwm2I7JZZaU68ToKzt-EmXrnSQzaKcqYCeeyaIV-_tP24Vl_Zm1gJSZRBxcJXVYWzvnwmZN8FIR-RtEe_qO6Sy0-vvUzWXWBIIEJFRbOBHChZhpP2VIDw8gEP6rc1KqUXwNmxO9tMwALqy1SyeA7O-0MGgeNpFNAsxVS_OSy6GVklCvOaeXk_zzH2HAR-gfpCVWmkL4L1h1Uo-bHOOLcnv3EfL5o_xI63xQtIDcNDPPHqS_w9oW5E0NJPogRSpvdYPRGrB7kz4F0vytMsCC4_5SsFRUDxuD_4HUsPGINJkmFYLNFfwkREt4UA'

        # Enter Casting Director token
        self.DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBDb09HYnU3TGJveThoTzhGRXhHdyJ9.eyJpc3MiOiJodHRwczovL3lvemRtci51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTE2OTYxNjc3NzU1MDYyNTIyMjEiLCJhdWQiOiJmaW5hbCIsImlhdCI6MTY4MDM2MTExNiwiZXhwIjoxNjgwNDQ3NTE2LCJhenAiOiI3RWprMWx0RThqa2x6SElHQkRBak1mVUpXQm9STk91VyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9yIiwiZ2V0Om1vdmllIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.JHPwyFffYSx9_byOyX0lLw4slfDV731-GWVZFcxM4Q4ZhjF36257UNPTXdpTz2M05Rs_CenRzWvE8v3VRV6aVUFM-B9uaVOW-m4K_jCRFRp1VqMdIpnZ8IBOKiWtP4VdKz9QkCeW964LYy3jDbQOP9EIPdcch8oDlw735BsBQU1riq0snYpLYV2zytYHwxq9YlLGS8OAMiOCLrzVKdaZw4YQuZ_8fu8Js-wkF9iXXO9zx0kfQAoaJHj0KC8EQrCNNU72VsnBKngz2jzPRpC7PHsauJzD9Qh5UqQ8qKPNkWGMFlPPU7I49fg0stloNq8D1LMuQpLjrUqLFKtCqNiBag'

        # Enter Casting Assistant token
        self.ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBDb09HYnU3TGJveThoTzhGRXhHdyJ9.eyJpc3MiOiJodHRwczovL3lvemRtci51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQyODQ2M2EwMDY2YTZlZWU5MzFhYmU1IiwiYXVkIjoiZmluYWwiLCJpYXQiOjE2ODAzNjExNDIsImV4cCI6MTY4MDQ0NzU0MiwiYXpwIjoiN0VqazFsdEU4amtsekhJR0JEQWpNZlVKV0JvUk5PdVciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvciIsImdldDptb3ZpZSJdfQ.o7ii_6zfAwubgil0IaFrWaadFw3U-kzTviX7dFpMiOjEkrgMgKrpcKr5nNpBhYSbGtCRRMVv2HS14GqIsCqcXfkrR9_2PS2Y08YgEnprxfoBBovD-cgwL-YzNELySj_6peBdWlTxJncpSiOR44e5czWTi2FXxaB79sMD21Ehrb9hyNFxMoewy_pb6gQEFcF9G3TsAtYeTkB155OGOqEVSs3gBr_tR-SRsgmY8tziGJd15Qk5--XKGV20jBS_Ev0ANWDJggCR4v5xC-svICpMBK_SFkeBuIeYVbCrp1en2bMndWoqA1_Nz0t2HmJQxV4S7BoHYVcbtgsh9dBhPpGMzg'

        # Enter token with no permissions
        self.NONE_TOKEN = ''

    def get_headers(self, type: str = None):
        if type == None or type == 'executive':
            return {'Authorization': f'Bearer {self.EXECUTIVE_TOKEN}'}
        elif type == 'director':
            return {'Authorization': f'Bearer {self.DIRECTOR_TOKEN}'}
        elif type == 'assistant':
            return {'Authorization': f'Bearer {self.ASSISTANT_TOKEN}'}
        elif type == 'none':
            return {'Authorization': f'Bearer {self.NONE_TOKEN}'}

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
        res = self.client().get('/actors', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['number_actors'], len(Actor.query.all()))
    
    # Get Failure
    def test_get_actors_bad_method(self):
        res = self.client().delete('/actors', headers=self.get_headers())
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
        res = self.client().post('/actors', headers=self.get_headers(), json=new_actor)
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
        res = self.client().post('/actors', headers=self.get_headers(), json=new_actor)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # Patch Success
    def test_patch_actors_success(self):
        actor = Actor(name='Test Actor', age=30, gender='Male')
        Actor.insert(actor)

        res = self.client().patch(f'/actors/{actor.id}', headers=self.get_headers(), json={'name': 'Modified Actor'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    # Patch Failure
    def test_patch_actors_bad_request(self):
        res = self.client().patch(f'/actors/999', headers=self.get_headers(), json={'name': 'Modified Actor'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')

    # Delete Success
    def test_delete_actors_success(self):
        actor = Actor(name='Test Actor', age=30, gender='Male')
        Actor.insert(actor)

        res = self.client().delete(f'/actors/{actor.id}', headers=self.get_headers())
        data = json.loads(res.data)

        actor = Actor.query.get(actor.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(actor, None)

    # Delete Failure
    def test_delete_actors_bad_request(self):
        res = self.client().delete(f'/actors/999', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')
    

    
    # ---------------
    # TESTING MOVIES
    # ---------------

    # Success
    def test_get_movies_success(self):
        res = self.client().get('/movies', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['number_movies'], len(Movie.query.all()))
    
    # Failure
    def test_get_movies_bad_method(self):
        res = self.client().delete('/movies', headers=self.get_headers())
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
        res = self.client().post('/movies', headers=self.get_headers(), json=new_movie)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added_movie']['title'], 'Good Movie')
    
    # Post Failure
    def test_post_movies_bad_data(self):
        new_movie = {
            'title': 'Good Movie'
        }
        res = self.client().post('/movies', headers=self.get_headers(), json=new_movie)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    # Patch Success
    def test_patch_movies_success(self):
        sample_date = datetime.now()
        movie = Movie(title='Test Movie', release_date=sample_date)
        Movie.insert(movie)

        res = self.client().patch(f'/movies/{movie.id}', headers=self.get_headers(), json={'title': 'Modified Movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Patch Failure
    def test_patch_movies_bad_request(self):
        res = self.client().patch(f'/movies/999', headers=self.get_headers(), json={'name': 'Modified Movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')
    
    # Delete Success
    def test_delete_movies_success(self):
        sample_date = datetime.now()
        movie = Movie(title='Test Movie', release_date=sample_date)
        Movie.insert(movie)

        res = self.client().delete(f'/movies/{movie.id}', headers=self.get_headers())
        data = json.loads(res.data)

        movie = Movie.query.get(movie.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(movie, None)
    
    # Delete Failure
    def test_delete_movies_bad_request(self):
        res = self.client().delete(f'/movies/999', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'page not found')
    

    # ---------------
    # TESTING RBAC
    # ---------------

    # Test Executive Role
    def test_delete__movie_executive(self):
        sample_date = datetime.now()
        movie = Movie(title='Test Movie', release_date=sample_date)
        Movie.insert(movie)

        # Here I am making sure to use the Executive role's token
        res = self.client().delete(f'/movies/{movie.id}', headers=self.get_headers('executive'))
        data = json.loads(res.data)

        movie = Movie.query.get(movie.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(movie, None)
    
    def test_post_actors_executive(self):
        new_actor = {
            'name': 'John Doe',
            'age': 35,
            'gender': 'male'
        }
        res = self.client().post('/actors', headers=self.get_headers('executive'), json=new_actor)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['added_actor']['name'], 'John Doe')
        self.assertEqual(data['added_actor']['age'], 35)
        self.assertEqual(data['added_actor']['gender'], 'male')

    
    # Test Director Role
    def test_patch_movies_director(self):
        sample_date = datetime.now()
        movie = Movie(title='Test Movie', release_date=sample_date)
        Movie.insert(movie)

        res = self.client().patch(f'/movies/{movie.id}', headers=self.get_headers('director'), json={'title': 'Modified Movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_delete_movies_director_fail(self):
        sample_date = datetime.now()
        movie = Movie(title='Test Movie', release_date=sample_date)
        Movie.insert(movie)

        res = self.client().delete(f'/movies/{movie.id}', headers=self.get_headers('director'))

        self.assertEqual(res.status_code, 403)


    # Test Assistant Role
    def test_get_actors_assistant(self):
        res = self.client().get('/actors', headers=self.get_headers('assistant'))
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['number_actors'], len(Actor.query.all()))
    
    def test_post_movies_assistant_bad(self):
        new_actor = {
            'name': 'John Doe',
            'age': 35,
            'gender': 'male'
        }
        res = self.client().post('/actors', headers=self.get_headers('assistant'), json=new_actor)
        
        self.assertEqual(res.status_code, 403)


# Make the tests conveniently executable 
if __name__ == "__main__":
    unittest.main()