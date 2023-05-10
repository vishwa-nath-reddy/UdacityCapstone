# Full Stack Movie Chain API Backend

## Motivation
I wanted to challenge myself to come up with a real life scenario and try to model the api as close as possible, also I wanted to prove myself that I have learnt all topics end to end through this project

## About
This project is intended to help people involved in movie industry, here we have simplified the participants to 3 parties, party 1 are the directors  and producers who are involved in making a movie and party 2 are the theatre owners who run the films and own theatres and party 3 i.e public who wants to watch movies, since these parties are critical to the industry, they all have different priorities hence, the app is designed to ensure all parties are satisfied
There are 4 types of users here
1. General Public
2. Theatre Owner
3. Movie Director
4. Movie Producer

1. General Public :
  a. They can access all movies and venues (theatres) with basic details
  b. They can also search for a movie, and see all theatres hosting the movie and the movie timings
  c. They can check by venue and get all movies run in a particular theatre id

2. Theatre Owner:
  a. Theatre owner can charge for a movie in form of rent, and add or delete or modify venue and shows
  b. Theatre Owner can also access sensitive information about all movies in all theatres

3. Movie Director:
  a. Can access sensitive information about a movie 
  b. Can modify movie properties

4. Movie Producer:
  a. Can delete / add / patch / access sensitive movie information
  b. He sets the ticket prices and budget of movie


## Application hosting link

https://capstone-zokq.onrender.com

## Authorization and accessing api's
1. Sensitive information is available only on logging in and passing the jwt token for each request
2. I've tried to implement the auth0 in app itself but, the token so generated was not access token but identity token, despite multiple tries could not figure it
3. Hence for all requests it is recommended to pass jwt obtained post logging here

# Click here to login to authenticate

https://dev-ex65k2q24qccu08f.us.auth0.com/authorize?audience=Movies&response_type=token&client_id=xSSpIpdRmYoyVWt1nQ8vbV9vdTPs9uZN&redirect_uri=https://127.0.0.1:3000/callback

## Requests and expected format with examples
#### GET `/`
##### Accessability intended to
Everyone
##### Point of endpoint 
This is the first page you see when you access the link, helps user to explore their available options, and tells the server is up
sample CURL:curl --location 'https://capstone-zokq.onrender.com/'

#### GET `/movies`
##### Accessability intended to
Everyone
##### Point of endpoint 
This is the page where you can access all movies available in this ecosystem
sample CURL:curl --location 'https://capstone-zokq.onrender.com/movies'

#### GET `/venues`
##### Accessability intended to
Everyone
##### Point of endpoint 
This is the page where you can access all venues available in this ecosystem
sample CURL:curl --location 'https://capstone-zokq.onrender.com/venues'

#### GET `/movies/<Movie_id_number>`
##### Accessability intended to
Everyone
##### Point of endpoint 
This page gives all venues where movie with id 1 is running
sample CURL:curl --location 'https://capstone-zokq.onrender.com/movies/1'

#### GET `/venues/<venue_id_number>`
##### Accessability intended to
Everyone
##### Point of endpoint 
This page gives all movies being played in venue 1
sample CURL:curl --location 'https://capstone-zokq.onrender.com/venues/1'


#### POST `/venues/create`
##### Accessability intended to
Theatre Owners
##### Point of endpoint 
Setting up new venue
sample CURL:curl --location 'https://capstone-zokq.onrender.com/venues/create' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
    "name":"IMAX1",
    "city":"New York City",
    "state": "New York",
    "address":"Stree 1 wall Street",
    "capacity":300,
    "contact_number":"12345678"
}'

#### GET `/venues/owner/<movie_id>`
##### Accessability intended to
Theatre Owners
##### Point of endpoint 
To see movie details along with day charge for the movie and its ticket price and show details
sample CURL:curl --location 'https://capstone-zokq.onrender.com/venues/owner/1' \
--header 'Authorization: Bearer <token>'

#### PATCH `/venues/change/<venue_id>`
##### Accessability intended to
Theatre Owners
##### Point of endpoint 
To modify venue details like charges, name etc
sample CURL:curl --location --request PATCH 'https://capstone-zokq.onrender.com/venues/change/1' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
    "name":"IMAX1",
    "city":"New York City",
    "state": "New York",
    "address":"Stree 1 wall Street",
    "capacity":300,
    "contact_number":"12345678990"
}'
  
#### DELETE `/venues/delete/<venue_id>`
##### Accessability intended to
Theatre Owners
##### Point of endpoint 
To delete venue 
sample CURL:curl --location --request DELETE 'https://capstone-zokq.onrender.com/venues/delete/2' \
--header 'Authorization: Bearer <token>'
 
  
#### POST `/shows/create`
##### Accessability intended to
Theatre Owners
##### Point of endpoint 
To create show by matching venue and movie 
sample CURL:curl --location 'https://capstone-zokq.onrender.com/shows/create' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
    "datetime":"2023-01-01",
    "venue_id":1,
    "movie_id":1,
    "movie_charge":5000
}'
  
 
#### PATCH `/shows/change/<show_id>`
##### Accessability intended to
Theatre Owners
##### Point of endpoint 
To modify shows 
sample CURL:curl --location --request PATCH 'https://capstone-zokq.onrender.com/shows/change/1' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
    "datetime":"2023-01-01",
    "venue_id":1,
    "movie_id":1,
    "movie_charge":60000
}'
 
  
#### DELETE `/shows/delete/<show_id>`
##### Accessability intended to
Theatre Owners
##### Point of endpoint 
To delete shows 
sample CURL: curl --location --request DELETE 'https://capstone-zokq.onrender.com/shows/delete/1' \
--header 'Authorization: Bearer <token>'
  
  
#### GET `/movie/owner/<movie_id>`
##### Accessability intended to
Movie producers, directors
##### Point of endpoint 
To give exclusive information on a particular movie like budget, planned release date etc
sample CURL:curl --location 'https://capstone-zokq.onrender.com/movie/owner/1' \
--header 'Authorization: Bearer <token>'
  
#### POST `/movie/add`
##### Accessability intended to
Movie producers
##### Point of endpoint 
To add a new movie
sample CURL: curl --location 'https://capstone-zokq.onrender.com/movie/add' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
    "name":"Homecoming",
    "language":"English",
    "producer":"abc",
    "director":"def",
    "budget":500000,
    "actors":"a bv cd fe",
    "planned_release_date":"2023-01-01",
    "ticket_price":200
}'
  
  
#### PATCH `/movie/patch/<movie_id>`
##### Accessability intended to
Movie producers, directors
##### Point of endpoint 
To modify movie
sample CURL:curl --location --request PATCH 'https://capstone-zokq.onrender.com/movie/patch/1' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
    "name":"Homecoming",
    "language":"French",
    "producer":"abcg",
    "director":"defm",
    "budget":460000,
    "actors":"a bv cd fe",
    "planned_release_date":"2023-01-01",
    "ticket_price":200
}'

#### DELETE `/movie/delete/<movie_id>`
##### Accessability intended to
Movie producers
##### Point of endpoint 
To delete movie
sample CURL:curl --location --request DELETE 'https://capstone-zokq.onrender.com/movie/delete/3' \
--header 'Authorization: Bearer <token>'  
  
  
## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

The project requires Python 3.9. Using a virtual environment such as `pipenv` is recommended. Set up the project as follows:

```

pipenv shell
pipenv install

```
### Getting Started
Pre-requisites and Local Development
You should already have Python3, pip and node installed on your local machines To create a virtual environment on MacOS, run: python3 -m venv env To activate the virtual environment, run: source env/bin/activate

### About the Stack
Backend
On MacOS, to set up all the dependencies, run: pip install requirements.txt To run the application on your local machine, run: python3 app.py .The application is hosted on https://capstone-zokq.onrender.com/ and can also be run locally at https://127.0.0.1:3000/ . The PostgreSQL database is hosted on Render. If you want to run locally using your local databse, you can modify the following fields in the models.py file: app.config['SQLALCHEMY_DATABASE_URI']=<your_local_database_uri>
  
### Database Setup - cloud hosting on Render
  NOTE: I am not giving instructions to set up this application in heroku cause it is no longer free and I myself have used Render only.
To create all the tables needed for this application in local environment first set SLQALCHEMY_DATABASE_URI and then
  cd <this folder location>
  flask db upgrade
to create tables in Render you first need to set up PostgreSQL database in Render, then copy the `External Database URL` mentioned in connect drop down at the top right corner, post copying set the app.config['SQLALCHEMY_DATABASE_URI']= `External Database URL`, post that run
  cd <this folder location>
  flask db upgrade
If you want to run this application in Render then you can follow the instructions mentioned in https://render.com/docs/deploy-flask#:~:text=You%20can%20deploy%20a%20Flask,%2Dhello%2Dworld%20on%20GitHub.
  in the start command settings you need to fill the following:
`gunicorn app:app`
  rest of the instructions can be followed directly from the link provided above
  
### Dependencies
  This project heavily uses FLASK, SQLalchemy, POSTGRES to create and set up models, for authentication jwt's generated using Auth0 with access tokens are used.
  Reason for using this tech stack is that it is simple to deploy and can be scaled up easily, sqlAlchemy provides the abstraction to interact with all databases using a common syntax and postgres is the most commonly used free databases, flask is chosen because of the clarity in code and features which can be added on top of it, Auth0 is used for authentication because of its community support and ease of use
  
  Although the tech stack may be simple, but it gets the job done like helps to visualize the real world scenario effectively
  
With Postgres running, create a database:

```

sudo -u postgres createdb test

```

## Testing

To test the API, first create a test database in postgres and then execute the tests as follows:

```
sudo -u postgres createdb test
python test_app.py
```
