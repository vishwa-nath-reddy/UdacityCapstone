# Full Stack Movie Chain API Backend

## About

The project provides the backend to create theatre chain. 
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

https://fsnd-family-tree.herokuapp.com

## Authorization and accessing api's
1. Sensitive information is available only on logging in and passing the jwt token for each request
2. I've tried to implement the auth0 in app itself but, the token so generated was not access token but identity token, despite multiple tries could not figure it
3. Hence for all requests it is recommended to pass jwt obtained post logging here

# Click here to login to authenticate

`https://dev-ex65k2q24qccu08f.us.auth0.com/authorize?audience=Movies&response_type=token&client_id=xSSpIpdRmYoyVWt1nQ8vbV9vdTPs9uZN&redirect_uri=https://127.0.0.1:3000/callback`

### Retreiving data 

The allowed requests are as follows:
1.




## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

The project requires Python 3.9. Using a virtual environment such as `pipenv` is recommended. Set up the project as follows:

```

pipenv shell
pipenv install

```

### Database Setup

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
