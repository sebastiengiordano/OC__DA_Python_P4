'''Controller for the Chess Tournaments.

Classes:
    ApplicationController
    HomeMenuController
    GenerateReportsController
    ExitApplicationController

'''

from ..models.menus import Menu
from ..models.Tournament import Tournaments
from ..models.Player import Players
from ..views.menu_views import HomeMenuView, GenerateReportsMenuView
from .tournament_controller import (
    NewTournamentController,
    ChoiceTournamentController,
    GenerateTournamentsReportsController
    )
from .player_controller import (
    RankingUpdateController,
    AddPlayerController,
    ShowPlayerController
)


class ApplicationController:
    '''Controller which call all other controllers.

    All other controllers should return an instance of the
    next controller according to the expected behavior.

    '''

    def __init__(self):
        '''Constructs the necessary attribute of ApplicationController.

        Call Players.init() in order to recovered
        the saved data link to players.

        Call Tournaments.init() in order to recovered
        the saved data link to tournament.

        '''
        self.controller = None
        Players.init()
        Tournaments.init()

    def start(self):
        '''Call the home menu and wait for the next controller to call'''
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    '''Controller which generate the home menu, ask the
    user choice, then return the linked controller.'''

    def __init__(self):
        self._menu = Menu()
        self._view = HomeMenuView(self._menu)

    def __call__(self):
        # Generate the home menu
        self._menu.add(
            "auto",
            "Créer un nouveau tournoi",
            NewTournamentController())
        self._menu.add(
            "auto",
            "Lancer / Reprendre un tournoi",
            ChoiceTournamentController())
        self._menu.add(
            "auto",
            "Mettre à jour les classements",
            RankingUpdateController())
        self._menu.add(
            "auto",
            "Ajouter un joueur",
            AddPlayerController())
        self._menu.add(
            "auto",
            "Générer des rapports",
            GenerateReportsController())
        self._menu.add(
            "q",
            "Quitter l'application",
            ExitApplicationController())

        # Ask user choice
        user_choice = self._view.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
        return user_choice.handler


class GenerateReportsController:
    '''Controller which generate the reports menu, ask the
    user choice, then return the linked controller.'''

    def __init__(self):
        self._menu = Menu()
        self._view = GenerateReportsMenuView(self._menu)

    def __call__(self):
        # Generate the reports menu
        self._menu.add(
            "auto",
            "Afficher tous les acteurs par ordre alphabétique",
            ShowPlayerController("Name"))
        self._menu.add(
            "auto",
            "Afficher tous les acteurs par classement",
            ShowPlayerController("Ranking"))
        self._menu.add(
            "auto",
            "Afficher tous les tournois",
            GenerateTournamentsReportsController())
        self._menu.add(
            "a",
            "Allez au menu d'acceuil",
            HomeMenuController())
        self._menu.add(
            "q",
            "Quitter l'application",
            ExitApplicationController())

        # Ask user choice
        user_choice = self._view.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
        return user_choice.handler


class ExitApplicationController:
    '''Controller which aim to exit the application'''
    def __call__(self):
        return None
