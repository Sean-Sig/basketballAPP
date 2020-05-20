from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import uuid
from settings import app

db = SQLAlchemy(app)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.String(80), unique=True, nullable=False)
    teamName = db.Column(db.String(80), unique=True, nullable=False)
    playerIds = db.Column(db.PickleType(), nullable=True)

    def json(self):
        return {
            'teamId': self.teamId,
            'teamName': self.teamName,
            'playerIds': self.playerIds
            }

    def add_team(_teamName, _playerIds):
        _teamId = 'teamId=' + str(uuid.uuid4())
        new_team = Team(teamId=_teamId, teamName=_teamName, playerIds=_playerIds)
        db.session.add(new_team)
        db.session.commit()

    def get_all_teams():
        return [Team.json(team) for team in Team.query.all()]

    def get_team(_teamId):
        return Team.json(Team.query.filter_by(teamId=_teamId).first())

    def delete_team(_teamId):
        is_successful = Team.query.filter_by(teamId=_teamId).delete()
        db.session.commit()
        return bool(is_successful)
