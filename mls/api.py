import datetime
import json
from flask import Response
from sqlalchemy import extract
from mls import app
from mls.database import session
from mls.models import ScheduledGame, Conference, ClubStanding


@app.route('/schedule')
@app.route('/schedule/<int:year>')
@app.route('/schedule/<int:year>/<month>')
def schedule(year=None, month='all'):
    games = session.query(ScheduledGame)

    if not year:
        year = datetime.datetime.now().year

    # TODO: 2015 is only officially supported!
    if year not in [2014, 2015]:
        message = '{} is an invalid year for requests.'.format(year)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype='application/json')

    games = games.filter(extract('year', ScheduledGame.time) == year)

    if month != 'all':
        try:
            month = int(month)
        except ValueError:
            message = 'Invalid month provided: {}'.format(month)
            data = json.dumps({'message': message})
            return Response(data, 404, mimetype='application/josn')
        else:
            games = games.filter(extract('month', ScheduledGame.time) == month)

    games = games.all()

    data = json.dumps([game.as_dictionary() for game in games])
    return Response(data, 200, mimetype='application/json')


@app.route('/standings')
@app.route('/standings/all')
@app.route('/standings/<conference>')
def standings(conference='all'):
    """Returns a response with conference standings.
    Root url /standings responds with standings for both conferences and the
    alias /standings/all is provided for those that want to be explicit.
    """
    conferences = session.query(Conference)

    if conference != 'all':
        conference = conference.title() + ' Conference'

        if conference not in ['Eastern Conference', 'Western Conference']:
            message = 'Couldnot find {} conference'.format(conference)
            data = json.dumps({'message': message})
            return Response(data, 404, mimetype='application/json')

        conferences = conferences.filter(Conference.name == conference)
    conferences = conferences.all()

    data = json.dumps([c.as_dictionary() for c in conferences])
    print(data)
    return Response(data, 200, mimetype='application/json')


@app.route('/standings/<conference>/<int:rank>')
def standings_by_team(conference, rank):
    """Returns response for one team in conference with rank"""
    conference = conference.title() + ' Conference'
    if conference not in ['Eastern Conference', 'Western Conference']:
        message = 'Could not find {} conference'.format(conference)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype='application/json')

    if rank not in range(1, 11):
        message = 'Could not find team with rank {}'.format(rank)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype='application/json')

    conference = session.query(Conference). \
        filter(Conference.name == conference).one()
    club = session.query(ClubStanding). \
        filter(ClubStanding.rank == rank,
               ClubStanding.conference_id == conference.id).all()

    data = json.dumps([c.as_dictionary() for c in club])
    return Response(data, 200, mimetype='application/json')


@app.route('/conference/<id_>')
def conference_get(id_):
    """Provides another way to gather conference standings, this time by id"""
    conference = session.query(Conference).get(id_)

    if not conference:
        message = 'Could not find conference with id {}'.format(id_)
        data = json.dumps({'message': message})
        return Response(data, 404, mimetype='application/json')

    data = json.dumps(conference.as_dictionary())
    return Response(data, 200, mimetype='application/json')