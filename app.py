import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import requires_auth

"""
https://yozdmr.us.auth0.com/authorize?audience=final&response_type=token&client_id=7Ejk1ltE8jklzHIGBDAjMfUJWBoRNOuW&redirect_uri=http://127.0.0.1:5000/login-results
"""

# create and configure the app
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    # CORS stuff below
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # NOTE: Auth permissions below
    # get/post/patch/delete  :  actor/movie

    
    # ------------------------------
    # Routes
    # ------------------------------

    @app.route('/')
    def index():
        return jsonify({
            "success": True
        })



    # GET Routes ------------------------------

    # Gets all of the actors
    @app.route('/actors')
    @requires_auth('get:actor')
    def get_actors(payload):
        actors = Actor.query.all()
        if actors != None:
            formatted_actors = [actor.format() for actor in actors]
            
            return {
                "number_actors": len(formatted_actors),
                "actors": formatted_actors,
                "success": True
            }
        else:
            abort(400)


    # Gets all of the movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movie')
    def get_movies(payload):
        movies = Movie.query.all()
        if movies != None:
            formatted_movies = [movie.format() for movie in movies]
            
            return {
                "number_movies": len(formatted_movies),
                "movies": formatted_movies,
                "success": True
            }
        else:
            abort(400)

    # Gets actor by provided ID
    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actor')
    def get_actor(payload, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor != None and Actor.query.all() != None:
            return {
                "number_actors": len(Actor.query.all()),
                "actor": actor.format(),
                "success": True
            }
        else:
            abort(404)

    # Gets movie by provided ID
    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movie')
    def get_movie(payload, id):
        movie = Movie.query.filter_by(id=id).one_or_none()
        if movie != None and Movie.query.all() != None:
            return {
                "number_movies": len(Movie.query.all()),
                "movie": movie.format(),
                "success": True
            }
        else:
            abort(404)



    # POST Routes ------------------------------

    # Posts actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def post_actor(payload):
        data = request.get_json()

        if 'name' not in data or 'age' not in data or 'gender' not in data:
            abort(400)
        
        new_actor = Actor(
            name = data['name'],
            age = data['age'],
            gender = data['gender']
        )
        Actor.insert(new_actor)

        return {
            "added_actor": new_actor.format(),
            "success": True
        }

    # Posts movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def post_movie(payload):
        data = request.get_json()

        if 'title' not in data or 'release_date' not in data:
            abort(400)
        
        new_movie = Movie(
            title = data['title'],
            release_date = data['release_date']
        )
        Movie.insert(new_movie)

        return {
            "added_movie": new_movie.format(),
            "success": True
        }


    # PATCH Routes ------------------------------

    # Patches actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_actor(payload, id: int):
        data = request.get_json()
        
        actor = Actor.query.filter_by(id=id).one_or_none()

        if actor == None:
            abort(404)
        
        # Updating values
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']

        Actor.update(actor)

        return {
            "updated_actor": actor.format(),
            "success": True
        }

    # Patches movie
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def patch_movie(payload, id: int):
        data = request.get_json()
        
        movie = Movie.query.filter_by(id=id).one_or_none()

        if movie == None:
            abort(404)

        # Updating values
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = data['release_date']

        Movie.update(movie)

        return {
            "updated_movie": movie.format(),
            "success": True
        }



    # DELETE Routes ------------------------------

    # Deletes actor based on given ID
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id: int):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor == None:
            abort(404)

        formatted_actor = actor.format()
        Actor.delete(actor)
        
        return {
            "deleted_actor": formatted_actor,
            "success": True
        }

    # Deletes movie based on given ID
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id: int):
        movie = Movie.query.filter_by(id=id).one_or_none()
        if movie == None:
            abort(404)
        formatted_movie = movie.format()
        Movie.delete(movie)
        
        return {
            "deleted_movie": formatted_movie,
            "success": True
        }

    # ------------------------------
    # Error handlers
    # ------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "page not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "internal server error"
        }), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)