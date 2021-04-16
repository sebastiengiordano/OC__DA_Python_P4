from tinydb import TinyDB, Query

from ..models.menus import Menu
from ..models.Player import Players, Player
from ..models.Tournament import Tournaments
from ..views.menu_views import (
    HomeMenuView,
    RankingUpdateMenuView,
    ChoicePlayerMenuView)
from ..views.player_views import (
    AddPlayerView,
    PlayerListView,
    PlayerRankingUpdateView
    )
from .tournament_controller import (
    NewTournamentController,
    ChoiceTournamentController
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
        self.menu = Menu()
        self._view = RankingUpdateMenuView(self.menu)

    def __call__(self):
        self.menu.add(
            "auto",
            "Afficher la liste des joueurs",
            PlayerListController())
        self.menu.add(
            "auto",
            "Afficher la liste des joueurs par classement",
            PlayerListController("Ranking"))
        self.menu.add(
            "auto",
            "Afficher la liste des joueurs par nom",
            PlayerListController("Name"))
        self.menu.add(
            "auto",
            "Afficher la liste des joueurs par age",
            PlayerListController("Age"))
        self.menu.add(
            "a",
            "Allez au menu d'acceuil",
            HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            ExitApplicationController())

        # 2. Ask user choice
        user_choice = self._view.get_user_choice()

        # 3. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler


class PlayerListController:

    def __init__(self, list_filter=None):
        self.menu = Menu()
        self._menu_view = ChoicePlayerMenuView(self.menu)
        self._view = PlayerListView()
        if list_filter == "Ranking":
            self.players_list = self._sort_by_ranking()
        elif list_filter == "Name":
            self.players_list = self._sort_by_name()
        elif list_filter == "Age":
            self.players_list = self._sort_by_age()
        else:
            self.players_list = Players.players.copy()

    def __call__(self):
        # 1. Show the players list
        self._view.show_players(self.players_list)

        # 2. Ask player choice
        choice = self._view.get_player_choice()

        # 3. Generate the player ranking update menu
        self.menu.add(
            "auto",
            f"Modifier le classement du joueur n°{choice + 1}",
            PlayerRankingUpdateController(self.players_list[choice]))
        self.menu.add(
            "auto",
            "Revenir au menu principal",
            HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            ExitApplicationController())

        # 4. Ask user choice
        user_choice = self._menu_view.get_user_choice()

        # 5. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler

    def _sort_by_ranking(self):
        players_list = Players.players.copy()
        players_list.sort(key=lambda x: x.rank, reverse=True)
        return players_list

    def _sort_by_name(self):
        players_list = Players.players.copy()
        players_list.sort(key=lambda x: (x.name, x.firstname))
        return players_list

    def _sort_by_age(self):
        players_list = Players.players.copy()
        players_list.sort(key=lambda x: (x.birthday, x.name))
        return players_list


class PlayerRankingUpdateController:

    def __init__(self, player):
        self._player = player
        self._view = PlayerRankingUpdateView()

    def __call__(self):
        # Ask for new ranking
        rank = self._view.ask_for_new_ranking()
        # Ask for validation
        if self._view.ask_for_validation():
            # update rank
            self._player.rank = rank
            # Save the player in Players.player
            self._save_in_players_list()
            # Save the player in db_players.json
            self._save_in_db_players()
        # Go back to main menu
        return HomeMenuController()

    def _save_in_players_list(self):
        for player in Players.players:
            if player == self._player:
                player = self._player
                break

    def _save_in_db_players(self):
        db_players = TinyDB(
            'ChessTournaments/models/database/db_players.json')
        query = Query()
        serialized_player = self._player.serialize()
        player_filter = (
            (query.name == serialized_player["name"])
            & (query.firstname == serialized_player["firstname"])
            & (query.birthday == serialized_player["birthday"])
            & (query.sex == serialized_player["sex"]))
        db_players.update(
            serialized_player,
            player_filter)


class AddPlayerController:

    def __init__(self):
        self._players = Players.players
        self._view = AddPlayerView()

    def __call__(self):
        player_added = False
        # 1. Ask for player name
        name = self._view.get_player_name()

        # 2. Check if this name is already in Players.players list
        players_with_same_name = Players.is_player_exist(name)
        if len(players_with_same_name) > 0:
            # 2.1   There is at least one player with the same name
            # 2.1.1 Ask if one of this(these) player(s) is the player
            #   the user want to add
            player_added = self._view.ask_if_player_in_list(
                players_with_same_name)

        if not player_added:
            # 2.2 This is a new player, add to the Players.players list
            firstname = self._view.get_player_firstname()
            birthday = self._view.get_player_birthday()
            sex = self._view.get_player_sex()
            rank = self._view.get_player_rank()
            Players.add_player(
                Player(name, firstname, birthday, sex, rank))

        # Go back to main menu
        return HomeMenuController()


class GenerateReportsController:

    def __init__(self):
        pass

    def __call__(self):
        pass


class ExitApplicationController:
    def __call__(self):
        return None
