from tinydb import TinyDB, Query

from ..models.Player import Players
from ..tools.tools_utils import datetime_to_str, is_date_format


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
        init():
            Deserialize all the tournaments in db_tournaments.json file
            and save them in tournaments list.
        add_tournament(tournament_to_add):
            Add new tournament in Tournaments.tournaments
            and db_tournaments.json.
    '''

    tournaments = []

    @classmethod
    def init(cls):
        '''Deserialize all the tournaments in db_tournaments.json file
        and save them in tournaments list.
        '''
        db_tournaments = TinyDB(
            'ChessTournaments/models/database/db_tournaments.json')
        for serialized_tournament in db_tournaments.all():
            tournaments.append(Tournanent.deserialize(serialized_tournament))

    @classmethod
    def add_tournament(cls, tournament_to_add):
        '''Add new tournament in db_tournament.json.
        '''
        db_tournament = TinyDB(
            './models/database/db_tournament.json')
        Tournaments.tournaments.append(tournament_to_add)
        return db_tournament.insert(tournament_to_add.serialize())

    @classmethod
    def update_tournament(cls, tournament_updated):
        '''Update a tournament in tournaments and db_tournament.json.
        '''
        db_tournament = TinyDB(
            './models/database/db_tournament.json')
        for index, tournament in enumerate(Tournaments.tournaments):
            if tournament == tournament_updated:
                Tournaments.tournaments[index] = tournament_updated

        db_tournament.update(
            tournament_updated.serialize(),
            Tournament.query_filter())


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
        _turns : []
            List which contains each turn of this tournaments
        turn_in_progress : int
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
        self._turns = []
        self.turn_in_progress = 1

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

            Return a dict() of these informations.
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
        tournament["turns"] = []
        for turn in self._turns:
            tournament["turns"].append(turn.serialize())
        tournament["turn_in_progress"] = self.turn_in_progress
        return tournament

    @classmethod
    def deserialize(self, serialized_tournament):
        '''Classmethod used to restore tournament information come from
        serialized tournament data.
        '''

        tournament = Tournament()
        tournament.name = serialized_tournament["name"]
        tournament.location = serialized_tournament["location"]
        tournament.start_date = is_date_format(
            serialized_tournament["start_date"])
        tournament.end_date = is_date_format(
            serialized_tournament["end_date"])
        tournament.numbers_of_turns = serialized_tournament["numbers_of_turns"]
        tournament.players = serialized_tournament["players"]
        tournament.time_control = serialized_tournament["time_control"]
        tournament.description = serialized_tournament["description"]
        for serialized_turn in serialized_tournament["turns"]:
            tournament._turns.append(Turn.deserialize(serialized_turn))
        tournament.turn_in_progress = serialized_tournament[
            "turn_in_progress"]
        return tournament

    @classmethod
    def query_filter(self, tournament):
        '''Return a Query objet to search a specific
        tournament in a TinyDB.
        '''
        query = Query()
        tournament_filter = (
            (query.name == tournament.name)
            & (query.location == tournament.location)
            & (query.start_date == datetime_to_str(tournament.start_date))
            & (query.end_date == datetime_to_str(tournament.end_date))
            & (query.numbers_of_turns == tournament.numbers_of_turns)
            & (query.time_control == tournament.time_control)
            & (query.description == tournament.description))
        return tournament_filter

class Turn:
    '''Class which represent one turn of a tournament.

    Attributes
    ----------
        current_round : str
            Indicate the current round.
        matchs : []
            List which contains each match of this turn

    Methods
    -------
        add_tournament(tournament_to_add):
            Add new tournament in Tournaments.tournaments
            and db_tournaments.json.
    '''

    def __init__(self, round_number, matchs):
        self.current_round = "Round " + str(round_number)

        self.matchs = matchs

    def serialize(self):
        '''Method used to cast turn information in str or int type.

            Return a dict() of these informations.
        '''
        turn = {}
        turn["round"] = self.current_round
        matchs = []
        for player_1, player_2 in self.matchs:
            matchs.append((
                [Players.get_player_id(player_1[0]), player_1[1]],
                [Players.get_player_id(player_2[0]), player_2[1]]
                ))
        turn["matchs"] = matchs
        return turn

    @classmethod
    def deserialize(self, serialized_turn):
        '''Classmethod used to restore turn information come from
        serialized turn data.
        '''
        current_round = serialized_turn["round"]
        matchs = []
        for turn in serialized_turn["round"]:
            serialized_player_1 = turn[0]
            serialized_player_2 = turn[1]
            player_1 = [
                Players.get_player_by_id(serialized_player_1[0]),
                serialized_player_1[1]
                ]
            player_2 = [
                Players.get_player_by_id(serialized_player_2[0]),
                serialized_player_2[1]
                ]
            matchs.append((player_1, player_2))
        return Turn(current_round, matchs)
