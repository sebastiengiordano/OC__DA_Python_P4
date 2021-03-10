class Tournament:

    def __init__(self):
        self.name = ""
        self.location = ""
        self.start_date = ""
        self.end_date = ""
        self.numbers_of_turns = 4
        self.players = []
        self.time_control = ""
        self.description = "Il va falloir écrire quelque chose d'ultra long pour tester la découpe du message. En plus il faudra que ça veuille dire quelque chose cette histoire, non ? De plus, il semblerait que le message s'affiche bien dans son cadre ! C'est vraiment une très très bonne nouvelle. J'espère que le responsable du tournoi en sera ravi."

        self._time_control_type = {
            "1": "Bullet",
            "2": "Blitz",
            "3": "Coup rapide"}

    @property
    def time_control_type(self):
        return self._time_control_type
