from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class Conference(Base):
    __tablename__ = 'conference'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    clubs = relationship('ClubStanding',
                         cascade="all, delete-orphan",
                         backref='conference',
                         order_by='ClubStanding.rank')

    def as_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'clubs': [club.as_dictionary() for club in self.clubs]
        }


class ClubStanding(Base):
    __tablename__ = 'club_standing'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    points = Column(Float, nullable=False)
    games_played = Column(Integer, nullable=False)
    points_per_game = Column(Float, nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    ties = Column(Integer, nullable=False)
    goals_for = Column(Integer, nullable=False)
    goals_against = Column(Integer, nullable=False)
    goals_difference = Column(Integer, nullable=False)
    home_goals_for = Column(Integer, nullable=False)
    home_goals_difference = Column(Integer, nullable=False)
    road_goals = Column(Integer, nullable=False)
    road_goals_difference = Column(Integer, nullable=False)

    conference_id = Column(Integer,
                           ForeignKey('conference.id',
                                      onupdate='CASCADE',
                                      ondelete='CASCADE'),
                           nullable=False)

    def as_dictionary(self):
        return {
            'id': self.id,
            'rank': self.rank,
            'name': self.name,
            'points': self.points,
            'games_played': self.games_played,
            'points_per_game': self.points_per_game,
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'goals_for': self.goals_for,
            'goals_against': self.goals_against,
            'goals_difference': self.goals_difference,
            'home_goals_for': self.home_goals_for,
            'home_goals_difference': self.home_goals_difference,
            'road_goals': self.road_goals,
            'road_goals_difference': self.road_goals_difference,
            'conference_id': self.conference_id
        }


class ScheduledGameBroadcaster(Base):
    __tablename__ = 'scheduled_game_broadcaster'

    scheduled_game_id = Column(Integer, ForeignKey('scheduled_game.id',
                                                   ondelete='CASCADE'),
                               primary_key=True)
    broadcaster_id = Column(Integer, ForeignKey('broadcaster.id',
                                                ondelete='CASCADE'),
                            primary_key=True)


class ScheduledGame(Base):
    __tablename__ = 'scheduled_game'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    home_team = Column(String, nullable=False)
    home_score = Column(Integer, nullable=False, default=0)
    away_team = Column(String, nullable=False)
    away_score = Column(Integer, nullable=False, default=0)
    matchcenter_url = Column(String, nullable=False)

    broadcasters = relationship('Broadcaster',
                                secondary='scheduled_game_broadcaster',
                                backref='scheduled_games')

    def as_dictionary(self):
        return {
            'id': self.id,
            'time': self.time.isoformat(),
            'home_team': self.home_team,
            'home_score': self.home_score,
            'away_team': self.away_team,
            'away_score': self.away_score,
            'matchcenter_url': self.matchcenter_url,
            'broadcasters': [broadcaster.as_dictionary()
                             for broadcaster in self.broadcasters]
        }


class Broadcaster(Base):
    __tablename__ = 'broadcaster'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def as_dictionary(self):
        return {
            'id': self.id,
            'name': self.name
        }