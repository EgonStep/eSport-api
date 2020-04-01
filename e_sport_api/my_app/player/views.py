import json
from flask import Blueprint, abort
from flask_restful import Resource, reqparse
from e_sport_api.my_app.player.models import Player
from e_sport_api.my_app import api, db

player = Blueprint('player', __name__)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('nickname', type=str)
parser.add_argument('team', type=str)
parser.add_argument('position', type=str)
parser.add_argument('assistance', type=int)
parser.add_argument('kills', type=int)
parser.add_argument('deaths', type=int)
parser.add_argument('games', type=int)
parser.add_argument('victories', type=int)


@player.route("/")
@player.route("/home")
def home():
    return "Create Players"


class PlayerAPI(Resource):
    def get(self, id=None, page=1):
        if not id:
            players = Player.query.paginate(page, 10).items
        else:
            players = [Player.query.get(id)]
        if not players:
            abort(404)

        res = {}
        for ppl in players:
            res[ppl.id] = {
                'name': ppl.name,
                'nickname': ppl.nickname,
                'team': ppl.team,
                'position': ppl.position,
                'assistance': ppl.assistance,
                'kills': ppl.kills,
                'deaths': ppl.deaths,
                'games': ppl.games,
                'victories': ppl.victories,
                'kda': str(round(ppl.kda, 2)),
                'win_per': str(round(ppl.win_per, 2))
            }

        return json.dumps(res)

    def post(self):
        args = parser.parse_args()
        ppl = populate_player(args, None)
        db.session.add(ppl)
        db.session.commit()

        res = create_response(ppl)
        return json.dumps(res)

    def delete(self, id):
        ppl = Player.query.get(id)
        db.session.delete(ppl)
        db.session.commit()

        res = {'id': id}
        return json.dumps(res)

    def put(self, id):
        ppl = Player.query.get(id)
        args = parser.parse_args()
        populate_player(args, ppl)
        db.session.commit()

        res = create_response(ppl)
        return json.dumps(res)


api.add_resource(
    PlayerAPI,
    '/api/players',
    '/api/players/<int:id>',
    '/api/players/<int:id>/<int:pages>',
)


def populate_player(args, ppl):
    name = args['name']
    nickname = args['nickname']
    team = args['team']
    position = args['position']
    assistance = args['assistance']
    kills = args['kills']
    deaths = args['deaths']
    games = args['games']
    victories = args['victories']

    if ppl is not None:
        ppl.name = name
        ppl.nickname = nickname
        ppl.team = team
        ppl.position = position
        ppl.assistance = assistance
        ppl.kills = kills
        ppl.deaths = deaths
        ppl.games = games
        ppl.victories = victories
        return
    else:
        return Player(name, nickname, team, position, assistance, kills, deaths, games, victories)


def create_response(ppl):
    res = {ppl.id: {
        'name': ppl.name,
        'nickname': ppl.nickname,
        'team': ppl.team,
        'position': ppl.position,
        'assistance': ppl.assistance,
        'kills': ppl.kills,
        'deaths': ppl.deaths,
        'games': ppl.games,
        'victories': ppl.victories,
        'kda': str(round(ppl.kda, 2)),
        'win_per': str(round(ppl.win_per, 2))
    }}
    return res
