import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Actor, Movie

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
    @app.route('/actors', methods=['GET'])
    def get_actors():
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
    def get_movies():
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
    def get_actor(id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        if actor != None and Actor.query.all() != None:
            return {
                "number_actors": len(Actor.query.all()),
                "actors": actor.format(),
                "success": True
            }
        else:
            abort(404)

    # Gets movie by provided ID
    @app.route('/movies/<int:id>', methods=['GET'])
    def get_movie(id):
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
    def post_actor():
        data = request.get_json()
        
        new_actor = Actor(
            name = data['name'],
            age = data['age'],
            gender = data['gender']
        )
        Actor.insert(new_actor)

        return {
            "added_actor": new_actor,
            "success": True
        }

    # Posts movie
    @app.route('/movies', methods=['POST'])
    def post_movie():
        data = request.get_json()
        
        new_movie = Movie(
            title = data['title'],
            release_date = data['date']
        )
        Movie.insert(new_movie)

        return {
            "added_movie": new_movie,
            "success": True
        }


    # PATCH Routes ------------------------------

    # Patches actor
    @app.route('/actors/<int:id>', methods=['PATCH'])
    def patch_actor(id: int):
        data = request.get_json()
        
        actor = Actor.query.filter_by(id=id)
        
        # Updating values
        actor.name = data['name']
        actor.age = data['age']
        actor.gender = data['gender']

        Actor.update(actor)

        return {
            "updated_actor": actor,
            "success": True
        }

    # Patches movie
    @app.route('/movies/<int:id>', methods=['PATCH'])
    def patch_movie(id: int):
        data = request.get_json()
        
        movie = Movie.query.filter_by(id=id)

        # Updating values
        movie.title = data['title']
        movie.release_date = data['date']

        Movie.update(movie)

        return {
            "updated_movie": movie,
            "success": True
        }



    # DELETE Routes ------------------------------

    # Deletes actor based on given ID
    @app.route('/actor/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        actor = Actor.query.filter_by(id=id)
        formatted_actor = actor.format()
        Actor.delete(actor)
        
        return {
            "deleted_actor": formatted_actor,
            "success": True
        }

    # Deletes movie based on given ID
    @app.route('/movie/<int:id>', methods=['DELETE'])
    def delete_movie(id):
        movie = Movie.query.filter_by(id=id)
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
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

    return app



if __name__ == '__main__':
    app = create_app()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)