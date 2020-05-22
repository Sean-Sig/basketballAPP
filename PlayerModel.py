from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import uuid
from settings import app

db = SQLAlchemy(app)

subs = db.Table('subs',
    db.Column('playerId', db.String, db.ForeignKey('players.playerId')),
    db.Column('gameId', db.String, db.ForeignKey('games.gameId'))
)

class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    gameId = db.Column(db.String(80), nullable=False)
    gameName = db.Column(db.String(80), nullable=False)
    playerStats = db.relationship('Stats', backref='statOwner')

    def json(self):
        return {
            'gameId': self.gameId,
            'gameName': self.gameName
            }

    def add_new_game(_gameName):
        _gameId = 'gameId=' + str(uuid.uuid4())
        new_game = Games(gameId=_gameId, gameName=_gameName)
        db.session.add(new_game)
        db.session.commit()

    def get_all_games():
        return [Games.json(game) for game in Games.query.all()]

    def add_player_to_game(_gameId, _playerId):
        game = Games.query.filter_by(gameId=_gameId).first()
        player = Player.query.filter_by(playerId=_playerId).first()
        Stats.add_player_stats(_playerId, _gameId)
        game.currentPlayers.append(player)
        db.session.commit()

    def get_players_of_game(_gameId):
        game = Games.query.filter_by(gameId=_gameId).first()
        return [Player.json(player) for player in game.currentPlayers]

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    playerId = db.Column(db.String(80), nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    jerseyNumber = db.Column(db.Integer)
    position = db.Column(db.String(80))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    playerStats = db.relationship('Stats', backref='owner')
    gameCenter = db.relationship('Games', secondary=subs, backref=db.backref('currentPlayers', lazy='dynamic'))

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

class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    stat_owner = db.Column(db.String(80), db.ForeignKey('players.playerId'), nullable=False)
    game_owner = db.Column(db.String(80), db.ForeignKey('games.gameId'), nullable=False)

    def json(self):
        return {
            'game_owner': self.game_owner,
            'stat_owner': self.stat_owner,
            'points': self.points
        }

    def get_all_stats():
        return [Stats.json(stat) for stat in Stats.query.all()]

    def get_player_stats(_playerId):
        player_to_find = Player.query.filter_by(playerId=_playerId).first()
        return ['playerProfile',[Player.json(player_to_find)]] + ['stats', [Stats.json(stat) for stat in player_to_find.playerStats]]

    def add_player_stats(_stat_owner, _game_owner):
        _points = 0
        new_stats = Stats(stat_owner=_stat_owner, game_owner=_game_owner, points=_points)
        db.session.add(new_stats)
        db.session.commit()

    def get_player_stats_in_game(_playerId, _gameId):
        player_to_find = Player.query.filter_by(playerId=_playerId).first()
        for i in player_to_find.playerStats:
            if i.game_owner == _gameId:
                return ['playerProfile',[Player.json(player_to_find)]] + ['stats', [Stats.json(i)]]

    def __repr__(self):
        stat_object = {
            'game_owner': self.game_owner,
            'stat_owner': self.stat_owner,
            'points': self.points
        }
        return json.dumps(stat_object)
