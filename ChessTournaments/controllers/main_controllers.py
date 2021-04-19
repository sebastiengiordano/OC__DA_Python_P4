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

    def __init__(self):
        self.controller = None
        Players.init()
        Tournaments.init()

    def start(self):
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    def __init__(self):
        self.menu = Menu()
        self._view = HomeMenuView(self.menu)

    def __call__(self):
        # Generate the home menu
        self.menu.add(
            "auto",
            "Créer un nouveau tournoi",
            NewTournamentController())
        self.menu.add(
            "auto",
            "Lancer / Reprendre un tournoi",
            ChoiceTournamentController())
        self.menu.add(
            "auto",
            "Mettre à jour les classements",
            RankingUpdateController())
        self.menu.add(
            "auto",
            "Ajouter un joueur",
            AddPlayerController())
        self.menu.add(
            "auto",
            "Générer des rapports",
            GenerateReportsController())
        self.menu.add(
            "q",
            "Quitter l'application",
            ExitApplicationController())

        # Ask user choice
        user_choice = self._view.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
        return user_choice.handler


class GenerateReportsController:

    def __init__(self):
        self.menu = Menu()
        self._view = GenerateReportsMenuView(self.menu)

    def __call__(self):
        # Generate the reports menu
        self.menu.add(
            "auto",
            "Afficher tous les acteurs par ordre alphabétique",
            ShowPlayerController("Name"))
        self.menu.add(
            "auto",
            "Afficher tous les acteurs par classement",
            ShowPlayerController("Ranking"))
        self.menu.add(
            "auto",
            "Afficher tous les tournois",
            GenerateTournamentsReportsController())
        self.menu.add(
            "a",
            "Allez au menu d'acceuil",
            HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            ExitApplicationController())

        # Ask user choice
        user_choice = self._view.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
        return user_choice.handler


class ExitApplicationController:
    def __call__(self):
        return None
