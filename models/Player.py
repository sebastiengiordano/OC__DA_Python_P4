from tinydb import TinyDB, Query

from ..tools.tools_utils import (
    is_date_format,
    datetime_to_str
)


class Players:
    '''Class which represent the players of the tournaments.

    Class Attributes
    ----------
        players : []
            List of instance of Player
            Update at init with data come from
            './models/database/db_players.json'.

    Methods
    -------
        add_player(player_to_add):
            Add new player in Players.players and db_players.json.
        is_player_exist(name):
            Classmethod which return a list which contains
            all players with the same name.
    '''

    players = []

    @classmethod
    def init(cls):
        db_players = TinyDB(
            './models/database/db_players.json')
        for serialized_player in db_players.all():
            player = Player.deserialize(serialized_player)
            Players.players.append(player)

    @classmethod
    def add_player(cls, player_to_add):
        '''Add new player in Players.players and db_players.json.

            Check if player_to_add isn't already in Players.players list.
            If its not the case, the player is added to this list
            and in db_players.json.
        '''
        if isinstance(player_to_add, Player):
            player_find = False
            for player in Players.players:
                if player_to_add == player:
                    player_find = True
                    break
            if not player_find:
                Players.players.append(player_to_add)
                return cls._serialize_player(player_to_add)

    @classmethod
    def is_player_exist(cls, name):
        '''Return a list of class Player which
        contains all players with the same name.
        '''
        query = Query()
        db_players = TinyDB(
            './models/database/db_players.json')
        return [
            Player.deserialize(player) for
            player in db_players.search(query.name == name)]

    @classmethod
    def _serialize_player(cls, player):
        db_players = TinyDB(
            './models/database/db_players.json')
        return db_players.insert(player.serialize())

    @classmethod
    def get_player_by_id(cls, id):
        '''Return Player instance according to its id the db_players.json.
        '''
        db_players = TinyDB(
            './models/database/db_players.json')
        player_serialize = db_players.get(doc_id=id)
        return Player.deserialize(player_serialize)

    @classmethod
    def get_player_id(cls, player):
        '''Return the id of the player in the db_players.json.
        '''
        db_players = TinyDB(
            './models/database/db_players.json')
        query = Query()
        player = Player.serialize(player)
        el = db_players.get(
            (query.name == player["name"])
            & (query.firstname == player["firstname"])
            & (query.birthday == player["birthday"])
            & (query.sex == player["sex"])
        )
        return el.doc_id


class Player:
    '''Class which represent a player.

    Attributes
    ----------
        _name : str
            Name of the player.
        _firstname : str
            Firstname of the player.
        _birthday : datetime.date
            Birthday of the player.
        _sex : str
            Sex of the player.
        _rank : int
            Player ranking.

    Methods
    -------
        name :
            Getter for the _name attribute.
        firstname :
            Getter for the _firstname attribute.
        birthday :
            Getter for the _birthday attribute.
        sex :
            Getter for the _sex attribute.
        rank :
            Getter and setter for the _rank attribute.
        serialize :
            Method used to cast player information in str or int type.
            Return a dict() of these information.
        deserialize :
        classmethod used to restore player information come from
        './models/database/db_players.json'.

    Special Methods
    -------
        eq :
            Compare the players name, firstname, birthday, sex.
            If their equal, return true. Otherwise return False.
        len :
            Return the size of the name + firstname + blank space.
    '''

    def __init__(self, name, firstname, birthday, sex, rank=0):
        self._name = name
        self._firstname = firstname
        self._birthday = birthday
        self._sex = sex
        self._rank = rank

    def __eq__(self, player):
        if isinstance(player, Player):
            equal = (
                self._name == player._name
                and self._firstname == player._firstname
                and self._birthday == player._birthday
                and self._sex == player._sex)
            if equal:
                return True
        return False

    def __len__(self):
        return len(self._name) + len(self._firstname) + 1

    def __str__(self):
        '''Special method used for debug only.
        '''
        print_display = (
            f"\n Nom: {self._name}"
            f"\n Prénom: {self._firstname}"
            f"\n Anniversaire: {self._birthday}"
            f"\n Sexe: {self._sex}"
            f"\n Rank: {str(self._rank)}")

        return print_display

    @property
    def name(self):
        '''Getter for the name attribute.
        '''
        return self._name

    @property
    def firstname(self):
        '''Getter for the firstname attribute.
        '''
        return self._firstname

    @property
    def birthday(self):
        '''Getter for the birthday attribute.
        '''
        return self._birthday

    @property
    def sex(self):
        '''Getter for the sex attribute.
        '''
        return self._sex

    @property
    def rank(self):
        '''Getter for the _rank attribute.
        '''
        return self._rank

    @rank.setter
    def rank(self, rank):
        '''Setter for the _rank attribute.
        '''
        if isinstance(rank, int) and rank >= 0:
            self._rank = rank

    def serialize(self):
        '''Method used to cast player information in str or int type.

            Return a dict() of these information.
        '''
        player = {}
        player["name"] = self._name
        player["firstname"] = self._firstname
        player["birthday"] = datetime_to_str(self._birthday)
        player["sex"] = self._sex
        player["rank"] = self._rank

        return player

    @classmethod
    def deserialize(cls, player):
        '''
            classmethod used to restore player information come from
            './models/database/db_players.json'.
        '''
        name = player["name"]
        firstname = player["firstname"]
        birthday = is_date_format(player["birthday"])
        sex = player["sex"]
        rank = player["rank"]

        return Player(name, firstname, birthday, sex, rank)
