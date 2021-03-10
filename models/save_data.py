from tinydb import TinyDB, Query


db_players = TinyDB('db_players.json')
db_tournaments = TinyDB('db_tournaments.json')


class save_new_players:
    def __init__(self, player):
        self.player = player

    def __call__(self):
        pass
