# Casting Agency API

## Description
The Casting Agency API is for a company responsible for creating and managing movies. Users will be able to view, add, edit or delete actors and movies based on what permissions they have.

This app has no frontend, so one would need to use Curl or an application like Postman to be able to access all of the features appropriately. 

## Dependencies
This project uses Python verson 3.10.10, which can be downloaded from Python's official website [here](https://www.python.org/downloads/release/python-31010/).

### PIP libraries
Once you have Python installed and have navigated to the home directory of the project, you can download all of the PIP dependencies with the following command:
```
pip3 install -r requirements.txt
```
It is recommended you create a virtual environment before you install the PIP dependencies, to keep the project organized and prevent conflicts with other installed libraries.

Make sure to navigate to the home directory of the project before creating your virtual environment using the following command:
```
py -3.10 -m venv venv
```

## Database
This project uses Postgresql. In the `models.py`, there is a variable called *uri*, which gets the database path from the environment variable *DATABASE_URL*. You can set this variable manually or you can run the `setup.sh` file after setting the *DATABASE_URL* variable inside it to your path.

### Tables
This app has two tables:
- Movie: This table represents the movies in the database. It has *title* and *release_date* as its values.
- Actor: This table represents the actors in the database. It has *name*, *age* and *gender* as its values.
Each table also has *insert()*, *update()* and *delete()* functions defined in it to make updating the database look cleaner in the code. The tables also have a *format()* function that returns a row in the table in JSON format.

## Running the app
Once the PIP dependencies are installed and the database has been connected, you can run the app with the command ```python app.py```. This should run the app in your console. The app is hosted on the port *5000*.

## Routes

### GET '/'
Permission required: `none`
- Displays success in reaching the route
- Request arguments: None
- Returns: A JSON object with key "success"

Sample response:
~~~json
{
    "success": true
}
~~~

### GET '/actors'
Permission required: `get:actor`
- Displays all of the actors in the database
- Request arguments: None
- Returns: A JSON object with keys "actors" (which contains all of the actors in the database), "number_actors" and "success"

Sample response:
~~~json
{
    "actors": [
        {
            "age": 30,
            "gender": "Male",
            "id": 1,
            "name": "John Doe"
        }
    ],
    "number_actors": 1,
    "success": true
}
~~~


### GET '/movies'
Permission required: `get:movie`
- Displays all of the movies in the database
- Request arguments: None
- Returns: A JSON object with keys "movies" (which contains all of the movies in the database), "number_movies" and "success"

Sample response:
~~~json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 07 Apr 2023 14:30:15 GMT",
            "title": "Good Movie"
        }
    ],
    "number_movies": 1,
    "success": true
}
~~~


### GET '/actors/<int:id>'
Permission required: `get:actor`
- Displays the actor with the specified ID
- Request arguments: ID (in the route)
- Returns: A JSON object with keys "actor" (which contains the actor requested), "number_actors" and "success"

Sample response:
~~~json
{
    "actor": {
        "age": 30,
        "gender": "Male",
        "id": 1,
        "name": "John Doe"
    },
    "number_actors": 1,
    "success": true
}
~~~


### GET '/movies/<int:id>'
Permission required: `get:movie`
- Displays the movie with the specified ID
- Request arguments: ID (in the route)
- Returns: A JSON object with keys "movie" (which contains the movie requested), "number_movies" and "success"

Sample response:
~~~json
{
    "movie": {
        "id": 1,
        "release_date": "Fri, 07 Apr 2023 14:30:15 GMT",
        "title": "Good Movie"
    },
    "number_movies": 1,
    "success": true
}
~~~


### POST '/actors'
Permission required: `post:actor`
- Adds an actor to the database
- Request arguments: A JSON object with attributes "name", "age" and "gender". 
- Returns: A JSON object with keys "added_actor" (which contains the actor that was added) and "success".

Sample response:
~~~json
{
    "added_actor": {
        "age": 30,
        "gender": "Male",
        "id": 1,
        "name": "John Doe"
    },
    "success": true
}
~~~

### POST '/movies'
Permission required: `post:movie`
- Adds an actor to the database
- Request arguments: A JSON object with attributes "title", "release_date". 
- Returns: A JSON object with keys "added_movie" (which contains the movie that was added) and "success".

Sample response:
~~~json
{
    "added_movie": {
        "id": 1,
        "release_date": "Fri, 07 Apr 2023 14:30:15 GMT",
        "title": "Good Movie"
    },
    "success": true
}
~~~

### PATCH '/actors/<int:id>'
Permission required: `patch:actor`
- Updates an actor in the database
- Request arguments: ID (in the route), and A JSON object with at least one of the attributes "name", "age" and "gender". 
- Returns: A JSON object with keys "updated_actor" (which contains the actor that was added) and "success".

Sample response:
~~~json
{
    "success": true,
    "updated_actor": {
        "age": 30,
        "gender": "Modified",
        "id": 1,
        "name": "John Doe"
    }
}
~~~


### PATCH '/movies/<int:id>'
Permission required: `patch:movie`
- Updates a movie in the database
- Request arguments: ID (in the route), and A JSON object with at least one of the attributes "title" and "release_date". 
- Returns: A JSON object with keys "updated_movie" (which contains the movie that was updated) and "success".

Sample response:
~~~json
{
    "success": true,
    "updated_movie": {
        "id": 1,
        "release_date": "Fri, 07 Apr 2023 14:30:15 GMT",
        "title": "Modified Movie"
    }
}
~~~

### DELETE '/actors/<int:id>'
Permission required: `patch:actor`
- Deletes an actor in the database
- Request arguments: ID (in the route)
- Returns: A JSON object with keys "deleted_actor" (which contains the actor that was deleted) and "success".

Sample response:
~~~json
{
    "deleted_actor": {
        "age": 30,
        "gender": "Male",
        "id": 1,
        "name": "John Doe"
    },
    "success": true
}
~~~

### DELETE '/movies/<int:id>'
Permission required: `patch:actor`
- Deletes a movie in the database
- Request arguments: ID (in the route)
- Returns: A JSON object with keys "deleted_movie" (which contains the movie that was deleted) and "success".

Sample response:
~~~json
{
    "deleted_movie": {
        "id": 1,
        "release_date": "Fri, 07 Apr 2023 14:30:15 GMT",
        "title": "Modified Movie"
    },
    "success": true
}
~~~


## Authentication
This application uses Auth0 to run. The Auth0 API Domain and Audience should be stored in a file called `authinfo.env` which should be created by the user. The values should be stored in values called *AUTH0_DOMAIN* and *API_AUDIENCE* respectively.

The JWT token contains the permissions for the roles listed below:
### Casting Assistant
 - get:actor
 - get:movie

### Casting Director
 - All permissions a Casting Assistant has and...
 - post:actor
 - delete:actor
 - patch:actor
 - patch:movie

### Executive Producer
 - All permissions a Casting Assistant has and...
 - post:movie
 - delete:movie

## Testing
This app also has a file called `test.py` that stores several test cases. This file contains:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of authentication for each role

To connect the `test_app.py` to a database, you will need to create a file called `dbinfo.env`. This file should contain the database name, user, password and host. These values should be stored in the file as *DATABASE_TEST_NAME*, *DATABASE_USER*, *DATABASE_PASSWORD* and *DATABASE_HOST*, respectively.

An example of this is below:
~~~
DATABASE_TEST_NAME=final_test
DATABASE_USER=postgres
DATABASE_PASSWORD=password123
DATABASE_HOST=localhost:5432
~~~


To run the `test_app.py` file correctly, you will need to get the JWT tokens of each role and set them. You can set them in the `test_app.py` file [here](https://github.com/yozdmr/Udacity-Web-Dev-Capstone/blob/main/test_app.py#L27).

## Deployment
The app is hosted live on Heroku. The URL is below.
Heroku URL: https://udacity-capstone-yozdmr.herokuapp.com/

