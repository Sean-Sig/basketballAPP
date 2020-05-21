from flask import Flask, jsonify, request, Response
from PlayerModel import *
from settings import *
import json
from UserModel import User
from TeamModel import *
import jwt, datetime
from functools import wraps

players = Player.get_all_players()
teams = Team.get_all_teams()
stats = Stats.get_all_stats()

app.config['SECRET_KEY'] = 'meow'

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



# GET
@app.route("/players")
@token_required
def get_players():
    return jsonify({'players': Player.get_all_players()})

# GET player by playerId
@app.route('/players/<string:playerId>')
def get_player_by_playerId(playerId):
    return_value = Player.get_player(playerId)
    return jsonify(return_value)

def validUserObject(userObject):
    if ("username" in userObject and "password" in userObject):
        return True
    else:
        return False

# POST and validation
def validPlayerObject(playerObject):
    if ("firstName" in playerObject and "lastName" in playerObject and "jerseyNumber" and "position" and "height" and "weight" in playerObject):
        return True
    else:
        return False

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

@app.route("/stats", methods=['POST'])
def add_stats():
    request_data = request.get_json()
    Stats.add_player_stats(request_data['points'], request_data['owner'])
    response = Response("", status=201, mimetype='application/json')
    response.headers['Location'] = "/stats/" + str(request_data['owner'])
    return response

# GET stats by playerId
@app.route('/stats/<string:playerId>')
def get_stats_by_playerId(playerId):
    return_value = Stats.get_stats(playerId)
    return jsonify(return_value)

# PUT
# @app.route('/players/<string:playerId>', methods=['PUT'])
# def replace_player(playerId):
#     request_data = request.get_json()
#     Player.replace_player(isbn, request_data['name'], request_data['price'])
#     response = Response("", status=204)
#     return response


# PATCH
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

# PATCH
@app.route('/teams/<string:teamId>', methods=['PATCH'])
def update_team(teamId):
    request_data = request.get_json()
    if ("playerIds" in request_data):
        Team.add_team_members(teamId, request_data['playerIds'])

    response = Response("", status=204)
    response.headers['Location'] = "/teams/" + str(teamId)
    return response

# DELETE
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

# DELETE
@app.route('/teams/<string:teamId>', methods=['DELETE'])
def delete_team(teamId):
    if (Team.delete_team(teamId)):
        response = Response("", status=204)
        return response

    invalidPlayerObjectErrorMsg = {
        "error": "Team with the teamId number that was provided was not found, so therefore unable to delete team"
    }
    response = Response(json.dumps(invalidPlayerObjectErrorMsg), status=404, mimetype='application/json')
    return response


# GET all teams
@app.route("/teams")
def get_teams():
    return jsonify({'teams': Team.get_all_teams()})

# GET team by teamId
# hereree
@app.route('/teams/<string:teamId>')
def get_team_by_teamId(teamId):
    return_value = Team.get_team(teamId)
    return jsonify(return_value)

# POST create a team
@app.route('/createTeam', methods=['POST'])
def create_team():
    request_data = request.get_json()

    Team.add_team(request_data['teamName'], request_data['playerIds'])
    response = Response("", status=201, mimetype='application/json')
    response.headers['Location'] = "/teams/" + str(request_data['teamName'])
    return response

# MAIN
if __name__ == "__main__":
    app.run(port=5000)
