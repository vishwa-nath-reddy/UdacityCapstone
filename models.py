from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from os import environ as env
from flask_migrate import Migrate

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vishwa:OjyIkfIaAQfmm4Mvg9O7ropwjUIJFV4K@dpg-ch9uahusi8uqs8mvbiag-a.oregon-postgres.render.com/movies_jtyq'
#postgres://vishwa:OjyIkfIaAQfmm4Mvg9O7ropwjUIJFV4K@dpg-ch9uahusi8uqs8mvbiag-a.oregon-postgres.render.com/movies_jtyq
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer,nullable=False)
    contact_number = db.Column(db.String(120), nullable=False)
    shows = db.relationship('Show', back_populates='venue')



    def __repr__(self):
        return f'Venue ID : {self.id} , Venue Name : {self.name}'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print('did not delete')
            print(e)

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(e)
    
    def public(self):
        return {
            'Theatre Name':self.name,
            'Location':self.address,
            'Contact Number': self.contact_number
        }

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    producer = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    actors = db.Column(db.String, nullable=False)
    planned_release_date = db.Column(db.DateTime(), nullable=False)
    shows = db.relationship('Show', back_populates='movie')
    ticket_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Movie ID : {self.id} , Movie Name : {self.name}'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print('did not delete')
            print(e)

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(e)

    def public(self):
        return {
            'Movie Name':self.name,
            'Primary Language':self.language,
            'Cast': self.actors,
            'Director':self.director,
            'Release':self.planned_release_date
        }
    
    def producer_spl(self):
        return {
            'Movie Name':self.name,
            'Primary Language':self.language,
            'Cast': self.actors,
            'Director':self.director,
            'Release':self.planned_release_date,
            'Budget': self.budget,
            'Ticket Price':self.ticket_price
        }

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    venue = db.relationship('Venue', back_populates='shows')
    movie = db.relationship('Movie', back_populates='shows')
    movie_charge = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Theatre Name : {self.venue_id}, Movie : {self.movie_id}'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print('did not delete')
            print(e)

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            print(e)

    def theatre_owner(self):
        return {
            'Movie ID':self.movie_id,
            'Movie Running Cost':self.movie_charge,
            'Movie Timings': self.datetime
        }