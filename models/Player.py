from tinydb import TinyDB, Query

from ..tools.tools_utils import is_date_format


class Players:
    """Class which represent players.

    Class Attributes
    ----------
    players : []
        List of instance of Player
        Update at init with data come from
        'ChessTournaments/models/database/db_players.json'.

    Methods
    -------
    add_player(player_to_add):
        Add new player in Players.players and db_players.json.
    is_player_exist(name):
        Classmethod which return a list which contains
        all players with the same name.
    """

    players = []

    def __init__(self):
        db_players = TinyDB(
            'ChessTournaments/models/database/db_players.json')
        for serialized_player in db_players.all():
            player = Player.deserialize(serialized_player)
            Players.players.append(player)

    @classmethod
    def add_player(self, player_to_add):
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
                Players.players.append(player)
                return self._serialize_player(player)

    @classmethod
    def is_player_exist(self, name):
        '''Return a list which contains all players with the same name.
        '''
        query = Query()
        db_players = TinyDB(
            'ChessTournaments/models/database/db_players.json')
        return [Player.deserialize(player) for player in db_players.search(query.name == name)]

    def _serialize_player(self, player):
        query = Query()
        db_players = TinyDB(
            'ChessTournaments/models/database/db_players.json')
        player_serialize = player.serialize()
        db_players.insert(
            player_serialize,
            (query.name == player_serialize['name'])
            & (query['firstname'] == player_serialize['firstname'])
            & (query['birthday'] == player_serialize['birthday'])
            & (query['sex'] == player_serialize['sex']))


class Player:
    """Class which represent a player.

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
        rank :
            Getter and setter for the _rank attribute.
        serialize :
            Method used to cast player information in str or int type.
            Return a dict() of these information.
        deserialize :
        classmethod used to restore player information come from
        'ChessTournaments/models/database/db_players.json'.

    Special Methods
    -------
        eq :
            Compare the players name, firstname, birthday, sex.
            If their equal, return true. Otherwise return False.
        len :
            Return the size of the name + firstname + blank space.
    """

    def __init__(self, name, firstname, birthday, sex, rank=0):
        self._name = name
        self._firstname = firstname
        self._birthday = birthday
        self._sex = sex
        self._rank = rank

    def __eq__(self, player):
        if isinstance(player, Player):
            if (
                self._name == player._name
        and self._firstname  == player._firstname
        and self._birthday == player._birthday
        and self._sex == player._sex):
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
    def rank(self):
        '''Getter for the _rank attribute.
        '''
        return self._rank

    @rank.setter
    def rank(self, rank):
        '''Setter for the _rank attribute.
        '''
        self._rank = rank

    def serialize(self):
        '''Method used to cast player information in str or int type.

            Return a dict() of these information.
        '''
        player = {}
        player["name"] = self._name
        player["firstname"] = self._firstname
        player["birthday"] = (
            f"{self._birthday:%d}/"
            + str(self._birthday.month) + "/"
            + str(self._birthday.year))
        player["sex"] = self._sex
        player["rank"] = self._rank

        return player

    @classmethod
    def deserialize(self, player):
        '''
            classmethod used to restore player information come from
            'ChessTournaments/models/database/db_players.json'.
        '''
        name = player["name"]
        firstname = player["firstname"]
        birthday = is_date_format(player["birthday"])
        sex = player["sex"]
        rank = player["rank"]

        return Player(name, firstname, birthday, sex, rank)

    def player_id(self, player):
        '''Return the id of the player in the db_players.json.
        '''
        db_players = TinyDB(
            'ChessTournaments/models/database/db_players.json')
        query = Query()
        player = self.serialize()
        el = db_players.get(
            (query.name == self._name)
            & (query.firstname == self._firstname)
            & (query.birthday == player["birthday"])
            & (query.sex == self._sex)
        )
        return el.doc_id


def main():
    import datetime
    player = Player(
        "Giordano",
        "Sébastien",
        datetime.date(1977, 4, 1),
        "M",
        852
        )
    player_2 = Player(
        "Bonelli",
        "Marion",
        datetime.date(1978, 5, 22),
        "F"
        )

    players = Players()
    players.add_player(player)
    players.add_player(player_2)

    # L = [{'name': 'a', 'firstname': 'Paul', 'birthday': datetime.date(2001,1,11), 'sex': 'M', 'rank': 111},
    # {'name': 'b', 'firstname': 'Susie', 'birthday': datetime.date(1987,2,25), 'sex': 'F', 'rank': 112},
    # {'name': 'c', 'firstname': 'Jack', 'birthday': datetime.date(2000,3,6), 'sex': 'M', 'rank': 812},
    # {'name': 'd', 'firstname': 'Harietty', 'birthday': datetime.date(1999,6,16), 'sex': 'F', 'rank': 1312},
    # {'name': 'e', 'firstname': 'Pierre', 'birthday': datetime.date(1166,12,30), 'sex': 'M', 'rank': 2112},
    # {'name': 'f', 'firstname': 'Blandine', 'birthday': datetime.date(2020,9,17), 'sex': 'F', 'rank': 888}]
    # for dico in L:
    #     players.add_player(Player(dico["name"], dico["firstname"], dico["birthday"], dico["sex"], dico["rank"]))

    player_3 = Player(
        "L'Epine",
        "Thibault",
        datetime.date(1988, 2, 13),
        "M",
        1783
        )
    players.add_player(player_3)
    bonelli = Players.is_player_exist('Bonelli')
    print(bonelli)
    for player in bonelli:
        print(player)


if __name__ == "__main__":
    main()
