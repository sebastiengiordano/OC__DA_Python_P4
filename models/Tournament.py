from ..views import views_parameters

class Tournament:

    def __init__(self):
        self.name = ""
        self.location = ""
        self.date = ""
        self.numbers_of_turns = 4
        self.players = []
        self.time_control = ""
        self.description = "Il va falloir écrire quelque chose d'ultra long pour tester la découpe du message. En plus il faudra que ça veuille dire quelque chose cette histoire, non ? De plus, il semblerait que le message s'affiche bien dans son cadre ! C'est vraiment une très très bonne nouvelle. J'espère que le responsable du tournoi en sera ravi."

        self.time_control_type = {
            "1": "Bullet",
            "2": "Blitz",
            "3": "Coup rapide"}

    def max_lenght(self):
        max_lenght = []
        if len(self.description) \
            > views_parameters.DESCRIPTION_DISPLAY_MAX_SIZE:
            max_lenght.append(views_parameters.DESCRIPTION_DISPLAY_MAX_SIZE)
        max_lenght.append(
            len(self.name)
            + len("Nom : ")
            + views_parameters.TEXT_LEFT_SIDE_OFFSET
            )
        max_lenght.append(
            len(self.location)
            + len("Lieu : ")
            + views_parameters.TEXT_LEFT_SIDE_OFFSET
            )
        for player in self.players:
            max_lenght.append(
                len(player)
                + views_parameters.TEXT_LEFT_SIDE_OFFSET
                )
        max_lenght.append(
            len("Contrôle du temps : ")
            + len(self.time_control)
            + views_parameters.TEXT_LEFT_SIDE_OFFSET
            )
        max_lenght.sort()
        return max_lenght[-1]


