from ..models.menus import Menu
from ..models.Player import Players, Player
from ..views.menu_views import HomeMenuView
from ..views.player_views import AddPlayerView
from .tournament_controller import (
                                NewTournamentController,
                                ChoiceTournamentController
                                )


class ApplicationController:

    def __init__(self):
        self.controller = None
        Players.init()

    def start(self):
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()


class HomeMenuController:
    def __init__(self):
        self.menu = Menu()
        self._view = HomeMenuView(self.menu)

    def __call__(self):
        # 1. Generate the home menu
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

        # 2. Ask user choice
        user_choice = self._view.get_user_choice()

        # 3. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler


class RankingUpdateController:

    def __init__(self):
        pass

    def __call__(self):
        pass


class AddPlayerController:

    def __init__(self):
        self._players = Players.players
        self._view = AddPlayerView()

    def __call__(self):
        # 1. Ask for player name
        name = self._view.get_player_name()

        # 2. Check if this name is already in Players.players list
        players_with_same_name = Players.is_player_exist(name)
        if players_with_same_name == []:
            # 2.1 This is a new play, add to the Players.players list
            firstname = self._view.get_player_firstname()
            birthday = self._view.get_player_birthday()
            sex = self._view.get_player_sex()
            rank = self._view.get_player_rank()
            Players.add_player(
                Player(name, firstname, birthday, sex, rank))


class GenerateReportsController:

    def __init__(self):
        pass

    def __call__(self):
        pass


class ExitApplicationController:
    def __call__(self):
        return None
