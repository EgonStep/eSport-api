from e_sport_api.my_app import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    team = db.Column(db.String(100))
    position = db.Column(db.String(100))
    assistance = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    games = db.Column(db.Integer)
    victories = db.Column(db.Integer)
    kda = db.Column(db.Float)
    win_per = db.Column(db.Float)

    def __init__(self, name, nickname, team, position, assistance, kills, deaths, games, victories):
        self.name = name
        self.nickname = nickname
        self.team = team
        self.position = position
        self.assistance = assistance
        self.kills = kills
        self.deaths = deaths
        self.games = games
        self.victories = victories

        if deaths == 0:
            self.kda = kills + assistance
        else:
            self.kda = (kills + assistance) / deaths

        self.win_per = (victories / games) * 100

    def __repr__(self):
        return 'Player {0}'.format(self.id)
