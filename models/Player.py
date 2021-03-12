from ..tools.tools_utils import is_date_format

class Players:

    def __init__(self):
        self._players = []

    def add_player(self, player):
        if isinstance(player, Player):
            self._players.append(player)

    def serialize_player(self):
        for player in self._players:
            pass


class Player:

    def __init__(self, name, firstname, birthday, sex, rank=0):
        self._name = name
        self._firstname = firstname
        self._birthday = birthday
        self._sex = sex
        self._rank = rank

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank):
        self._rank = rank

    def serialize(self):
        player = {}
        player["name"] = self._name
        player["firstname"] = self._firstname
        birthday = self._birthday
        player["birthday"] = (
            f"{birthday:%d}/"
            f"{birthday:%m}/"
            f"{birthday:%Y}")
        player["sex"] = self._sex
        player["rank"] = self._rank
        
        return player

    @classmethod
    def deserialize(self, player):
        name = player["name"]
        firstname = player["firstname"]
        birthday = is_date_format(player["birthday"])
        sex = player["sex"]
        rank = player["rank"]

        return Player(name, firstname, birthday, sex, rank)

    def __str__(self):
        print_display = (
            f"\n Nom: {self._name}"
            f"\n Prénom: {self._firstname}"
            f"\n Anniversaire: {self._birthday}"
            f"\n Sexe: {self._sex}"
            f"\n Rank: {str(self._rank)}")

        return print_display


def main():
    player = Player(
        "Giordano",
        "Sébastien",
        "01/04/1977",
        "M",
        852
        )
    print(player)

    player.rank = 1112
    print(player)

    player_2 = Player(
        "Bonelli",
        "Marion",
        "22/05/1978",
        "F"
        )
    print(player_2)

if __name__ == "__main__":
    main()
