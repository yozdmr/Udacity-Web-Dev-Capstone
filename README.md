# Udacity-Web-Dev-Capstone
### The capstone project for the Udacity Full Stack Web Developer certification.

Heroku URL: https://udacity-capstone-yozdmr.herokuapp.com/

### The authentication is the sample one provided, with the roles below:

#### Casting Assistant
 - get:actor
 - get:movie
#### Casting Director
 - All permissions a Casting Assistant has and...
 - post:actor
 - delete:actor
 - patch:actor
 - patch:movie
#### Executive Producer
 - All permissions a Casting Assistant has and...
 - post:movie
 - delete:movie

To run the test_app.py file correctly, you will need to get the JWT tokens of each role and set them. The location in the file is [here](https://github.com/yozdmr/Udacity-Web-Dev-Capstone/blob/main/test_app.py#L27):
