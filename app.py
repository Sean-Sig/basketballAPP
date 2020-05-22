from flask import Flask, jsonify, request, Response
from PlayerModel import *
from settings import *
import json
from UserModel import User
import jwt, datetime
from functools import wraps

players = Player.get_all_players()
stats = Stats.get_all_stats()
games = Games.get_all_games()

app.config['SECRET_KEY'] = 'meow'

# CREATE ACCOUNT POST
@app.route('/createUser', methods=['POST'])
def create_user():
    request_data = request.get_json()
    if (validUserObject(request_data)):
        User.create_user(request_data['username'], request_data['password'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/createUser/" + str(request_data['username'])
        return response
    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid user object passed in request",
            "helpString": "Data passed in similar to this {'username': 'username', 'password': 'password'}"
        }
        response = Response(json.dumps(invalidUserObjectErrorMsg), status=400, mimetype='application/json');
        return response

# VALIDATE CREATE USER
def validUserObject(userObject):
    if ("username" in userObject and "password" in userObject):
        return True
    else:
        return False

# LOGIN
@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Resonse('', 401, mimetype='application/json')

# CREATE TOKEN
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401
    return wrapper


# GET ALL PLAYERS
@app.route("/players")
# @token_required
def get_players():
    return jsonify({'players': Player.get_all_players()})

# GET PLAYER BY playerId
@app.route('/players/<string:playerId>')
def get_player_by_playerId(playerId):
    return_value = Player.get_player(playerId)
    return jsonify(return_value)

# CREATE GAME
@app.route("/games", methods=['POST'])
def add_game():
    request_data = request.get_json()
    Games.add_new_game(request_data['gameName'])
    response = Response("", status=201, mimetype='application/json')
    response.headers['Location'] = "/games/" + str(request_data['gameName'])
    return response

# GET ALL GAMES
@app.route("/games")
# @token_required
def get_games():
    return jsonify({'games': Games.get_all_games()})

# ADD PLAYER TO GAME
@app.route("/playerToGame", methods=['POST'])
def add_player_game():
    request_data = request.get_json()
    Games.add_player_to_game(request_data['gameId'], request_data['playerId'])
    response = Response("", status=201, mimetype='application/json')
    response.headers['Location'] = "/playerToGame/" + str(request_data['gameId'])
    return response

# GET PLAYERS BY gameId
@app.route("/gameplayers/<string:gameId>")
# @token_required
def get_game_player(gameId):
    return jsonify({'team1': Games.get_players_of_game(gameId)})


# CREATE PLAYER
@app.route("/players", methods=['POST'])
def add_player():
    request_data = request.get_json()
    if (validPlayerObject(request_data)):
        Player.add_player(request_data['firstName'], request_data['lastName'], request_data['jerseyNumber'], request_data['position'], request_data['height'], request_data['weight'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/players/" + str(request_data['firstName'])
        return response
    else:
        invalidPlayerObjectErrorMsg = {
            "error": "Invalid player object passed in request",
            "helpString": "Data passed in similar to this {'firstName': 'firstName', 'lastName': 'lastname', 'price': 7.99, 'isbn': 484984}"
        }
        response = Response(json.dumps(invalidPlayerObjectErrorMsg), status=400, mimetype='application/json');
        return response

# VALIDATE CREATING PLAYER OBJECT
def validPlayerObject(playerObject):
    if ("firstName" in playerObject and "lastName" in playerObject and "jerseyNumber" and "position" and "height" and "weight" in playerObject):
        return True
    else:
        return False

# PATCH PLAYER
@app.route('/players/<string:playerId>', methods=['PATCH'])
def update_player(playerId):
    request_data = request.get_json()
    if ("position" in request_data):
        Player.update_player_position(playerId, request_data['position'])
    if ("jerseyNumber" in request_data):
        Player.update_player_jerseyNumber(playerId, request_data['jerseyNumber'])
    if ("weight" in request_data):
        Player.update_player_weight(playerId, request_data['weight'])
    if ("height" in request_data):
        Player.update_player_height(playerId, request_data['height'])

    response = Response("", status=204)
    response.headers['Location'] = "/players/" + str(playerId)
    return response

# DELETE PLAYER BY playerId
@app.route('/players/<string:playerId>', methods=['DELETE'])
def delete_player(playerId):
    if (Player.delete_player(playerId)):
        response = Response("", status=204)
        return response

    invalidPlayerObjectErrorMsg = {
        "error": "Player with the playerId number that was provided was not found, so therefore unable to delete player"
    }
    response = Response(json.dumps(invalidPlayerObjectErrorMsg), status=404, mimetype='application/json')
    return response

# GET stats by playerId
@app.route('/stats/<string:playerId>')
def get_stats_by_playerId(playerId):
    return_value = Stats.get_player_stats(playerId)
    return jsonify(return_value)

@app.route('/playerStatsGame')
def get_stats_of_player_game():
    request_data = request.get_json()
    return_value = Stats.get_player_stats_in_game(request_data['playerId'], request_data['gameId'])
    return jsonify(return_value)
# MAIN
if __name__ == "__main__":
    app.run(port=5000)
