from re import compile


DESCRIPTION_DISPLAY_MAX_SIZE = 30


class Tournament:

    def __init__(self):
        self.name = ""
        self.location = ""
        self.date = ""
        self.numbers_of_turns = 4
        self.players = []
        self.time_control = ""
        self.description = "Il va falloir écrire un truc ultra long pour tester la découpe du message. En plus il faudra que ça veuille dire quelque chose cette histoire, non ?"

        self.time_control_type = {
            "1": "Bullet",
            "2": "Blitz",
            "3": "Coup rapide"}

    def _is_date_format(self, string_to_test):
        date_format = compile(r"^(?:\d{2}\/){2}\d{4}$")
        if date_format.match(string_to_test):
            return True
        else:
            return False

    def max_lenght(self):
        if len(self.description) > DESCRIPTION_DISPLAY_MAX_SIZE:
            max_lenght = [DESCRIPTION_DISPLAY_MAX_SIZE]
        max_lenght.append(len(self.name) + len("Nom"))
        max_lenght.append(len(self.location) + len("Lieu"))
        for elem in self.players:
            max_lenght.append(len(elem[0]) + len(elem[1]) + 1)
        max_lenght.sort()
        return max_lenght[-1]


