from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Conference(Base):
    __tablename__ = 'conference'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    clubs = relationship('ClubStanding', backref='conference')


# Consider renaming this to just Standing and associate it with a team
# possibly dropping the name field too?
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
    conference_id = Column(Integer, ForeignKey('conference.id'), nullable=False)