from tinydb import TinyDB, Query

from ..tools.tools_utils import datetime_to_str


class Tournaments:
    '''Class which represent all the tournaments.

    Class Attributes
    ----------
        tournaments : []
            List of instance of tournament
            Update at init with data come from
            './models/database/db_players.json'.

    Methods
    -------
        add_tournament(tournament_to_add):
            Add new tournament in Tournaments.tournaments
            and db_tournaments.json.
    '''

    tournaments = []

    @classmethod
    def add_tournament(cls, tournament_to_add):
        '''Add new tournament in db_tournament.json.
        '''
        db_tournament = TinyDB(
            './models/database/db_tournament.json')
        cls.tournaments.append(tournament_to_add)
        return db_tournament.insert(tournament_to_add.serialize())


class Tournament:
    '''Class which represent a tournament.

    Attributes
    ----------
    name : str
        Name of the tournament.
    location : str
        Location of the tournament.
    start_date : datetime.date
        Start date of the tournament.
    end_date : datetime.date
        End date of the tournament.
    numbers_of_turns : int
        Number of rounds for this tournament.
    players : []
        List of players which participate to this tournament.
        Stored according to their id in db_players.json
    time_control : str
        time control of the tournament.
    description : str
        Description of the tournament.
    turns : []
        List which contains each turn of this tournaments
    _turn_in_progress : int
        Indicate the turn which will be played.

    Methods
    -------
    time_control_type :
        Return the time control type of this tournament.
    '''

    def __init__(self):
        self.name = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        self.numbers_of_turns = 4
        self.players = []
        self.time_control = ""
        self.description = "Il va falloir écrire quelque chose d'ultra long pour tester la découpe du message. En plus il faudra que ça veuille dire quelque chose cette histoire, non ? De plus, il semblerait que le message s'affiche bien dans son cadre ! C'est vraiment une très très bonne nouvelle. J'espère que le responsable du tournoi en sera ravi."
        self._turn_in_progress = 1

        self._time_control_type = {
            "1": "Bullet",
            "2": "Blitz",
            "3": "Coup rapide"}

    @property
    def time_control_type(self):
        '''Return the time control type of this kind of tournament.
        '''
        return self._time_control_type

    def serialize(self):
        '''Method used to cast tournament information in str or int type.

            Return a dict() of these information.
        '''

        tournament = {}
        tournament["name"] = self.name
        tournament["location"] = self.location
        tournament["start_date"] = datetime_to_str(self.start_date)
        tournament["end_date"] = datetime_to_str(self.end_date)
        tournament["numbers_of_turns"] = self.numbers_of_turns
        tournament["players"] = self.players
        tournament["time_control"] = self.time_control
        tournament["description"] = self.description
        tournament["turn_in_progress"] = self._turn_in_progress
        return tournament


class Turn:
    '''Class which represent one turn of a tournament.

    Attributes
    ----------
        current_round : str
            Indicate the current round.
        player_one : Player
            Instance of the first player which participate to this turn.
        player_two : Player
            Instance of the second player which participate to this turn.
        winner_id : int
            ID of the player which win this turn.

    Methods
    -------
        add_tournament(tournament_to_add):
            Add new tournament in Tournaments.tournaments
            and db_tournaments.json.
    '''

    @classmethod
    def serialize(self):
        '''Method used to cast turn information in str or int type.

            Return a dict() of these information.
        '''
        turn = {}
        return turn
