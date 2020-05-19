from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import uuid
from settings import app

db = SQLAlchemy(app)

class Player(db.Model):
    __tablename__ = 'players3'
    id = db.Column(db.Integer, primary_key=True)
    playerId = db.Column(db.String(80), nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    jerseyNumber = db.Column(db.Integer)
    position = db.Column(db.String(80))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    def json(self):
        return {
            'playerId': self.playerId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'jerseyNumber': self.jerseyNumber,
            'position': self.position,
            'height': self.height,
            'weight': self.weight
            }

    def add_player(_firstName, _lastName, _jerseyNumber, _position, _height, _weight):
        _playerId = 'playerId=' + str(uuid.uuid4())
        new_player = Player(playerId=_playerId, firstName=_firstName, lastName=_lastName, jerseyNumber=_jerseyNumber, position=_position, height=_height, weight=_weight)
        db.session.add(new_player)
        db.session.commit()

    def get_all_players():
        return [Player.json(player) for player in Player.query.all()]

    def get_player(_playerId):
        return Player.json(Player.query.filter_by(playerId=_playerId).first())

    def delete_player(_playerId):
        is_successful = Player.query.filter_by(playerId=_playerId).delete()
        db.session.commit()
        return bool(is_successful)

    def update_player_jerseyNumber(_playerId, _jerseyNumber):
        player_to_update = Player.query.filter_by(playerId=_playerId).first()
        player_to_update.jerseyNumber = _jerseyNumber
        db.session.commit()

    def update_player_position(_playerId, _position):
        player_to_update = Player.query.filter_by(playerId=_playerId).first()
        player_to_update.position = _position
        db.session.commit()

    def update_player_weight(_playerId, _weight):
        player_to_update = Player.query.filter_by(playerId=_playerId).first()
        player_to_update.weight = _weight
        db.session.commit()

    def update_player_height(_playerId, _height):
        player_to_update = Player.query.filter_by(playerId=_playerId).first()
        player_to_update.height = _height
        db.session.commit()
    #
    # def replace_player(_isbn, _name, _price):
    #     player_to_replace = Player.query.filter_by(isbn=_isbn).first()
    #     player_to_replace.price = _price
    #     player_to_replace.name = _name
    #     db.session.commit()

    def __repr__(self):
        player_object = {
            'playerId': self.playerId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'jerseyNumber': self.jerseyNumber,
            'position': self.position,
            'height': self.height,
            'weight': self.weight
        }
        return json.dumps(player_object)
