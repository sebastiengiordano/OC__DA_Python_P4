from ..models.menus import Menu
from ..views import HomeMenuView


class ApplicationController:

    def __init__(self):
        self.controller = None

    def start(self):
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        # 1. Generate the home menu
        self.menu.add(
            "auto",
            "Créer un nouveau tournoi",
            NewTournementController())
        self.menu.add(
            "auto",
            "Lancer / Reprendre un tournoi",
            StartTournementController())
        self.menu.add(
            "auto",
            "Mise à jour des classements",
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

        # 2. Ask user choice
        user_choice = self.view.get_user_choice()

        # 3. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler


class NewTournementController:
    pass


class StartTournementController:
    pass


class RankingUpdateController:
    pass


class AddPlayerController:
    pass


class GenerateReportsController:
    pass


class ExitApplicationController:
    def __call__(self):
        return None
