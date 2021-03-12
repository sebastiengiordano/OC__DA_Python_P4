from tinydb import TinyDB, Query


db_tournaments = TinyDB('db_tournaments.json')

class Tournament:
    """Class which represent a tournament.

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
    time_control : str
        time control of the tournament.
    description : str
        Description of the tournament.

    Methods
    -------
    time_control_type :
        Return the time control type of this tournament.
    """

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
        '''Return the time control type of this tournament.
        '''
        return self._time_control_type
