from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, \
    Table
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


class ClubStanding(Base):
    __tablename__ = 'club_standing'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    points = Column(Float, nullable=False)
    games_played = Column(Integer, nullable=False)
    pointers_per_game = Column(Float, nullable=False)
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


scheduled_game_broadcaster = \
    Table('scheduled_game_broadcaster',
          Base.metadata,
          Column('scheduled_game_id',
                 Integer,
                 ForeignKey('scheduled_game.id', ondelete='CASCADE')),
          Column('broadcaster_id',
                 Integer,
                 ForeignKey('broadcaster.id',
                            ondelete='CASCADE'))
          )


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
                                secondary=scheduled_game_broadcaster,
                                backref='scheduled_games')


class Broadcaster(Base):
    __tablename__ = 'broadcaster'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)