#!/usr/bin/env python3
"""Runs the development server for MLS Scraper."""
import os

import requests
import bs4

import dateutil.parser
from flask.ext.script import Manager

from mls_scraper import app
from mls_scraper.database import session
from mls_scraper.models import Conference, ClubStanding, Broadcaster, \
    ScheduledGame

manager = Manager(app)


@manager.command
def scrape_schedule():
    """Attempts to seed the database with the year's schedule.

    At this point, this command does not offer an opportunity to update an
    existing database.
    """
    # Drop existing DB rows before building
    session.query(Broadcaster).delete()
    session.query(ScheduledGame).delete()
    session.commit()

    # scrape season schedule
    # competition_type=46 is MLS Regular Season
    # there is also a param called 'month' which takes an integer argument
    # for the month, or the argument 'all'
    url = 'http://www.mlssoccer.com/schedule'
    payload = {'month': 'all', 'year': 2015, 'competition_type': 46}

    r = requests.get(url, params=payload)
    soup = bs4.BeautifulSoup(r.text)

    # select the dates
    dates = soup.select('div.schedule-page h3')

    # games for a specific date are an immediate sibling of the date
    # each table has a header and several rows for each game
    # each follow is a repeat of a template; some values are left empty
    games = []
    for date in dates:
        tr = date.find_next('tbody').tr
        while tr:
            game = {}

            td = tr.td  # time
            time = td.div.get_text(strip=True)
            if time == 'TBD':
                time = ''
            time = '%s %s' % (date.get_text(strip=True), time)
            game['time'] = dateutil.parser.parse(time)
            td = td.find_next_sibling('td')

            game['home_team'] = td.div.get_text(strip=True)
            td = td.find_next_sibling('td', class_='score')

            game['home_score'] = None
            game['away_score'] = None
            if td.div:
                scores = [int(x)
                          for x in td.div.get_text(strip=True).split('-')]
                # if an MLS team manages to score greater than...
                # 9?? hahaha never gonna happen!
                game['home_score'] = scores[0]
                game['away_score'] = scores[1]

            td = td.find_next_sibling('td', class_='away-team')
            game['away_team'] = td.div.get_text(strip=True)

            td = td.find_next_sibling('td')
            game['broadcasters'] = None
            if td.div.contents:
                broadcasts = td.div.find_all('strong')
                broadcasts = [b.get_text(strip=True) for b in broadcasts]
                game['broadcasters'] = broadcasts

            td = td.find_next_sibling('td')
            game['matchcenter_url'] = td.a.attrs.get('href')

            games.append(game)
            # index forward
            tr = tr.find_next_sibling('tr')

    broadcasters = add_broadcasters_to_db(games)
    add_scheduled_games_to_db(games, broadcasters)


def add_broadcasters_to_db(games):
    """Use the compiled list of scheduled games to load a dictionary of
    broadcasters for the remainder of the season so we can associate
    them with the games when we put them into the database

    Returns a dictionary of broadcasters ({name: database_object}) for utility.
    """
    broadcasters = {}

    for game in games:
        if game['broadcasters']:
            for broadcaster in game['broadcasters']:
                if broadcaster not in broadcasters.keys():
                    broadcaster_db = Broadcaster(name=broadcaster)
                    session.add(broadcaster_db)
                    session.commit()
                    broadcasters[broadcaster] = broadcaster_db

    return broadcasters


def add_scheduled_games_to_db(games, broadcasters):
    """Add scraped games to database"""
    for game in games:
        game_db = ScheduledGame(time=game['time'],
                                home_team=game['home_team'],
                                home_score=game['home_score'],
                                away_team=game['away_team'],
                                away_score=game['away_score'],
                                matchcenter_url=game['matchcenter_url'])

        for broadcaster in game['broadcasters']:
            game_db.broadcasters.append(broadcasters[broadcaster])

        session.add(game_db)
    session.commit()


@manager.command
def scrape_standings():
    """Scrape current MLS standings"""
    # Drop existing DB rows before building
    # Dropping conferences will also drop the clubs
    session.query(Conference).delete()
    session.commit()

    url = 'http://www.mlssoccer.com/standings'

    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text)

    eastern_table = soup.find('table', class_='standings-table')
    eastern_standings = gather_standings_from_table(eastern_table)

    western_table = eastern_table.find_next('table', class_='standings-table')
    western_standings = gather_standings_from_table(western_table)

    add_standings_to_db('eastern', eastern_standings)
    add_standings_to_db('western', western_standings)


def gather_standings_from_table(table):
    keys = ['rank', 'club', 'points', 'games_played', 'points_per_game',
            'wins', 'losses', 'ties', 'goals_for', 'goals_against',
            'goal_difference', 'home_goals_for', 'home_goals_difference',
            'road_goals', 'road_goals_difference']

    trs = table.tbody.find_all('tr')
    standings = []
    for tr in trs:
        standing = {}
        for key, stat in zip(keys, tr.find_all('td')):
            if key == 'club':
                standing[key] = stat.get_text(strip=True)
            elif key.endswith('_per_game'):
                standing[key] = float(stat.get_text(strip=True))
            else:
                standing[key] = int(stat.get_text(strip=True))
        standings.append(standing)

    return standings


def add_standings_to_db(conference_name, standings):
    name = "%s Conference" % conference_name.capitalize()
    conference = Conference(name=name)
    session.add(conference)
    session.commit()

    payload = []
    for club in standings:
        new_club = make_club_standing_from_object(club, conference)
        payload.append(new_club)

    session.add_all(payload)
    session.commit()


def make_club_standing_from_object(club, conference):
    return ClubStanding(rank=club['rank'],
                        name=club['club'],
                        points=club['points'],
                        games_played=club['games_played'],
                        pointers_per_game=club['points_per_game'],
                        wins=club['wins'],
                        losses=club['losses'],
                        ties=club['ties'],
                        goals_for=club['goals_for'],
                        goals_against=club['goals_against'],
                        goals_difference=club['goal_difference'],
                        home_goals_for=club['home_goals_for'],
                        home_goals_difference=club['home_goals_difference'],
                        road_goals=club['road_goals'],
                        road_goals_difference=club['road_goals_difference'],
                        conference=conference)


@manager.command
def run():
    port = int(os.environ.get('MLS_CONFIG_PORT', 8080))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    manager.run()