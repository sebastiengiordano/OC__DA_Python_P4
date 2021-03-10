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

    def __init__(self, name, firstname, birthday, sexe, rank):
        self._name = name
        self._firstname = firstname
        self._birthday = birthday
        self._sexe = sexe
        self._rank = rank

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank):
        self._rank = rank

    def __str__(self):
        print_display = (
            f"\n Nom: {self._name}"
            f"\n Prénom: {self._firstname}"
            f"\n Anniversaire: {self._birthday}"
            f"\n sexe: {self._sexe}"
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


if __name__ == "__main__":
    main()
