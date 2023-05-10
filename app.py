from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort, session
from models import Movie, Show, Venue, app, db
from auth.auth import AuthError, requires_auth

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for
from flask_migrate import Migrate

oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/authorize?audience=Movies&response_type=token&client_id=xSSpIpdRmYoyVWt1nQ8vbV9vdTPs9uZN&redirect_uri=https://127.0.0.1:3000/callback'
)


@app.route("/logout")
def logout():
    session.clear()
    print(session.keys())
    # print(session['user'])
    step = env.get("AUTH0_DOMAIN")
    return redirect('https://' + step + '/v2/logout')
    # return redirect('/')


# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/")
def home():
    data = {'success': True,
            'message': 'You can access movies and venues for free and search them as well',
            'special': 'If you want to do something then you must login and need to have permissions'}
    result = jsonify(data)
    return result


# Public end points

@app.route('/venues', methods=['GET'])
def venues():
    if request.method!='GET':
        abort(404)
    try:
        cityStateCombo = db.session.query(Venue).distinct().all()
        result = []
        print(cityStateCombo)
        for x in cityStateCombo:
            result.append(x.public())
        target = jsonify(result)
        return target
    except:
        abort(500)


@app.route('/movies', methods=['GET'])
def movies():
    if request.method!='GET':
        abort(404)
    try:
        print('movie')
        print(Movie)
        cityStateCombo = db.session.query(Movie).all()
        print(1)
        result = []
        print(cityStateCombo)
        for x in cityStateCombo:
            result.append(x.public())
        target = jsonify(result)
        return target
    except Exception as e:
        print(e)
        abort(500)


@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(*li,**yi):
    if request.method!='GET':
        abort(404)
    x=yi.get('venue_id')
    result = db.session.query(Show).filter(Show.venue_id == x).all()
    target = {}
    venue_details = db.session.query(Venue).filter(Venue.id == x).first().public()
    temp = []
    for x in result:
        base = {}
        base['Movie']: db.session.query(Movie.name).filter(Movie.id == x.movie_id).first()
        base['Timings']: x.datetime
        base['Ticket Price']: db.session.query(Movie.ticket_price).filter(Movie.id == x.movie_id).first()
        temp.append(base)
    venue_details['Movies details']: temp
    final = jsonify(venue_details)
    return final


@app.route('/movies/<int:movie_id>', methods=['GET'])
def show_movie(*li,**yi):
    if request.method!='GET':
        abort(404)
    x=yi.get('movie_id')
    result = db.session.query(Show).filter(Show.movie_id == x).all()
    target = {}
    Movie_details = db.session.query(Movie).filter(Movie.id == x).first().public()
    temp = []
    for x in result:
        base = {}
        base['Venue']: db.session.query(Venue.name).filter(Venue.id == x.venue_id).first()
        base['Timings']: x.datetime
        base['Ticket Price']: db.session.query(Movie.ticket_price).filter(Venue.id == x.venue_id).first()
        temp.append(base)
    Movie_details['Venue details']: temp
    final = jsonify(Movie_details)
    return final


# Theatre owner end points

@app.route('/venues/create', methods=['POST'])
@requires_auth('post:venue')
def create_venue_form(*ki):
    if request.method!='POST':
        abort(404)
    print('jere')
    body = request.get_json()
    print(body)
    if (
            'name' in body and 'city' in body and 'state' in body and 'address' in body and 'capacity' in body and 'contact_number' in body):
        newVenue = Venue(name=body.get('name'), city=body.get('city'), state=body.get('state'),
                         address=body.get('address'), capacity=body.get('capacity'),
                         contact_number=body.get('contact_number'))
        newVenue.insert()
        data = {
            'success': True,
            'venue': newVenue.public()
        }
        final = jsonify(data)
        return final
    else:
        abort(422)


@app.route('/venues/change/<int:venue_id>', methods=['PATCH'])
@requires_auth('patch:venue')
def modify_venue_form(*li,**yi):
    if request.method!='PATCH':
        abort(404)
    x=yi.get('venue_id')
    body = request.get_json()
    if (
            'name' in body and 'city' in body and 'state' in body and 'address' in body and 'capacity' in body and 'contact_number' in body):
        base = db.session.query(Venue).filter(Venue.id == x).first()
        if base == None:
            abort(422)
        else:
            base.name = body.get('name')
            base.city = body.get('city')
            base.state = body.get('state')
            base.address = body.get('address')
            base.capacity = body.get('capacity')
            base.contact_number = body.get('contact_number')
            base.update()
            data = {
                'success': True,
                'venue': base.public()
            }
            final = jsonify(data)
            return final
    else:
        abort(422)


@app.route('/venues/delete/<int:venue_id>', methods=['DELETE'])
@requires_auth('delete:venue')
def delete_venue_form(*li,**yi):
    if request.method!='DELETE':
        abort(404)
    x=yi.get('venue_id')
    base = db.session.query(Venue).filter(Venue.id == x).first()
    if base == None:
        abort(422)
    else:
        data = {
            'success': True,
            'venue': base.public(),
            'deleted': True
        }
        base.delete()
        final = jsonify(data)
        return final


@app.route('/venues/owner/<int:movie_id>', methods=['GET'])
@requires_auth('get:venue')
def show_venue_full(*li,**yi):
    if request.method!='GET':
        abort(404)
    x=yi.get('movie_id')
    print(x)
    try:
        all_shows = db.session.query(Show).filter(Show.venue_id == x).all()
        result = {}
        print(all_shows)
        result['venue Details'] = db.session.query(Venue).filter(Venue.id == x).first().public()
        print(result)
        show_details = []
        for x in all_shows:
            temp = {}
            temp['Movie Title'] = db.session.query(Movie).filter(Movie.id == x.movie_id).first().name
            temp['Ticket Price'] = db.session.query(Movie).filter(Movie.id == x.movie_id).first().ticket_price
            temp['language'] = db.session.query(Movie).filter(Movie.id == x.movie_id).first().language
            temp['Theatre Rent'] = x.movie_charge
            show_details.append(temp)
            print(temp)
        result['Show Details'] = show_details
        final = jsonify(result)
        print(final)
        return final
    except:
        abort(400)


@app.route('/shows/create', methods=['POST'])
@requires_auth('post:show')
def create_show_form(*ki):
    if request.method!='POST':
        abort(404)
    print('there')
    body = request.get_json()
    print(body)
    if ('datetime' in body and 'venue_id' in body and 'movie_id' in body and 'movie_charge' in body):
        if db.session.query(Movie).filter(
                Movie.id == int(body.get('movie_id'))).first() is not None and db.session.query(Venue).filter(
            Venue.id == int(body.get('venue_id'))).first() is not None:
            print('chp2')
            newVenue = Show(datetime=body.get('datetime'), venue_id=body.get('venue_id'), movie_id=body.get('movie_id'),
                            movie_charge=body.get('movie_charge'))
            newVenue.insert()
            print('chep3')
            data = {
                'success': True,
                'show': db.session.query(Movie.name).filter(Movie.id == int(body.get('movie_id'))).first().name,
                'timings': body.get('datetime')
            }
            final = jsonify(data)
            return final
        else:
            abort(404)
    else:
        abort(422)


@app.route('/shows/change/<int:id>', methods=['PATCH'])
@requires_auth('patch:show')
def modify_show_form(*li,**yi):
    if request.method!='PATCH':
        abort(404)
    x=yi.get('id')
    body = request.get_json()
    print(body)
    if ('datetime' in body and 'venue_id' in body and 'movie_id' in body and 'movie_charge' in body):
        if db.session.query(Show).filter(Show.id == x).first() is not None:
            base = db.session.query(Show).filter(Show.id == x).first()
            base.datetime = body.get('datetime')
            base.venue_id = body.get('venue_id')
            base.movie_id = body.get('movie_id')
            base.movie_charge = body.get('movie_charge')
            base.update()
            data = {
                'success': True,
                'show': db.session.query(Movie.name).filter(Movie.id == int(body.get('movie_id'))).first().name,
                'timings': body.get('datetime')
            }
            final = jsonify(data)
            return final
        else:
            abort(404)
    else:
        abort(422)


@app.route('/shows/delete/<int:id>', methods=['DELETE'])
@requires_auth('delete:show')
def delete_show_form(*li,**yi):
    if request.method!='DELETE':
        abort(404)
    x=yi.get('id')
    if db.session.query(Show).filter(Show.id == x).first() is not None:
        base = db.session.query(Show).filter(Show.id == x).first()
        base.delete()
        print('deleted')
        data = {
            'success': True,
            'show': db.session.query(Movie.name).filter(Movie.id == int(body.get('movie_id'))).first().name,
        }
        final = jsonify(data)
        return final
    else:
        abort(404)


# Movie Producer, director paths


@app.route('/movie/owner/<int:movie_id>', methods=['GET'])
@requires_auth('get:movie')
def show_movie_full(*li,**yi):
    if request.method!='GET':
        abort(404)
    x=yi.get('movie_id')
    try:
        result = db.session.query(Movie).filter(Movie.id == x).first().producer_spl()
        final = jsonify(result)
        return result
    except:
        abort(400)


@app.route('/movie/patch/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def edit_movie_full(*x,**y):
    if request.method!='PATCH':
        abort(404)
    print('alfa')
    print(x)
    print(y)
    print(type(y))
    movie_id=y.get('movie_id')
    print(movie_id)
    print(request.get_json())
    body = request.get_json()
    print(body)
    if (
            'name' in body and 'language' in body and 'producer' in body and 'director' in body and 'budget' in body and 'actors' in body and 'planned_release_date' in body and 'ticket_price' in body):
        if db.session.query(Movie).filter(Movie.id == movie_id).first() is not None:
            base = db.session.query(Movie).filter(Movie.id == movie_id).first()
            base.name = body.get('name')
            base.language = body.get('language')
            base.producer = body.get('producer')
            base.director = body.get('director')
            base.budget = body.get('budget')
            base.actors = body.get('actors')
            base.planned_release_date = body.get('planned_release_date')
            base.ticket_price = body.get('ticket_price')
            base.update()
            data = {
                'success': True,
                'Movie': db.session.query(Movie).filter(Movie.id == movie_id).first().producer_spl()
            }
            final = jsonify(data)
            return final
        else:
            abort(404)
    else:
        abort(422)


@app.route('/movie/add', methods=['POST'])
@requires_auth('post:movie')
def add_movie_full(ki):
    if request.method!='POST':
        abort(404)
    body = request.get_json()
    print('finally')
    print(body)
    if ('name' in body and 'language' in body and 'producer' in body and 'director' in body and 'budget' in body and 'actors' in body and 'planned_release_date' in body and 'ticket_price' in body):
        base = Movie(name=body.get('name'), language=body.get('language'), producer=body.get('producer'),
                     director=body.get('director'), budget=body.get('budget'), actors=body.get('actors'),
                     planned_release_date=body.get('planned_release_date'), ticket_price=body.get('ticket_price'))
        base.insert()
        data = {
            'success': True,
            'Movie': base.producer_spl()
        }
        final = jsonify(data)
        return final
    else:
        abort(422)


@app.route('/movie/delete/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie_full(*li,**yi):
    if request.method!='DELETE':
        abort(404)
    print(yi)
    x=yi.get('movie_id')
    if db.session.query(Movie).filter(Movie.id == x).first() is not None:
        base = db.session.query(Movie).filter(Movie.id == x).first()
        base.delete()
        data = {
            'success': True,
            'Movie': base.producer_spl()
        }
        final = jsonify(data)
        return final
    else:
        abort(404)


@app.errorhandler(422)
def impossible(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "cannot accept the request"
    }), 422


# @app.errorhandler(400)
# def missing(error):
#     return jsonify({
#         "success": False,
#         "error": 400,
#         "message": "cound not get the item"
#     }), 400
@app.errorhandler(404)
def incorrect(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "cound not get the item"
    }), 404


@app.errorhandler(500)
def internalservererror(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Error from server side"
    }), 500


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "request item not available or not present"
    }), 404


@app.errorhandler(AuthError)
def handling_authorization_errors(x):
    return jsonify({
        "success": False,
        "error": x.status_code,
        'message': x.error
    }), 401


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=env.get("PORT", 3000), debug=True)
