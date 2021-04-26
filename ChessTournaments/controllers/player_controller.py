'''Controller link to players management.

Classes:
    RankingUpdateController
    PlayerListController
    PlayerRankingUpdateController
    AddPlayerController
    ShowPlayerController

'''

from tinydb import TinyDB, Query

from . import main_controllers
from ..models.menus import Menu
from ..models.Player import Players, Player
from ..views.menu_views import (
    RankingUpdateMenuView,
    ChoicePlayerMenuView)
from ..views.player_views import (
    AddPlayerView,
    PlayerListView,
    PlayerRankingUpdateView
    )


class RankingUpdateController:
    '''Controller which generate the ranking update menu,
    ask the user choice, then return the linked controller.'''

    def __init__(self):
        self._menu = Menu()
        self._view = RankingUpdateMenuView(self._menu)

    def __call__(self):
        # Generate the reports menu
        self._menu.add(
            "auto",
            "Afficher la liste des joueurs",
            PlayerListController())
        self._menu.add(
            "auto",
            "Afficher la liste des joueurs par classement",
            PlayerListController("Ranking"))
        self._menu.add(
            "auto",
            "Afficher la liste des joueurs par nom",
            PlayerListController("Name"))
        self._menu.add(
            "auto",
            "Afficher la liste des joueurs par age",
            PlayerListController("Age"))
        self._menu.add(
            "a",
            "Allez au menu d'acceuil",
            main_controllers.HomeMenuController())
        self._menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # Ask user choice
        user_choice = self._view.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
        return user_choice.handler


class PlayerListController:
    '''Controller link to RankingUpdateController which show the sorted
    player list, ask which player to update or if the user want to go back
    to an upper menu, then return the appropriate controller'''

    def __init__(self, list_filter=None):
        self._menu = Menu()
        self._menu_view = ChoicePlayerMenuView(self._menu)
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
        # Show the players list
        self._view.show_players(self.players_list)

        # Ask player choice
        choice = self._view.get_player_choice()

        # Generate the player ranking update menu
        self._menu.add(
            "auto",
            f"Modifier le classement du joueur n°{choice + 1}",
            PlayerRankingUpdateController(self.players_list[choice]))
        self._menu.add(
            "a",
            "Allez au menu d'acceuil",
            main_controllers.HomeMenuController())
        self._menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # Ask user choice
        user_choice = self._menu_view.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
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
    '''Controller used to update the ranking of one player.'''

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
        return main_controllers.HomeMenuController()

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
    '''Controller which manages the addition of a new player,
    then return the HomeMenuController.'''

    def __init__(self):
        self._players = Players.players
        self._view = AddPlayerView()

    def __call__(self):
        player_added = False
        # Ask for player name
        name = self._view.get_player_name()

        # Check if this name is already in Players.players list
        players_with_same_name = Players.is_player_exist(name)
        if len(players_with_same_name) > 0:
            # There is at least one player with the same name
            #   Ask if one of this(these) player(s) is the player
            #   the user want to add
            player_added = self._view.ask_if_player_in_list(
                players_with_same_name)

        if not player_added:
            #   This is a new player, add to the Players.players list
            firstname = self._view.get_player_firstname()
            birthday = self._view.get_player_birthday()
            sex = self._view.get_player_sex()
            rank = self._view.get_player_rank()
            Players.add_player(
                Player(name, firstname, birthday, sex, rank))

        # Go back to main menu
        return main_controllers.HomeMenuController()


class ShowPlayerController(PlayerListController):
    '''Controller call by GenerateReportsController
    in order to show a sorted player list,
    then return the HomeMenuController.'''

    def __init__(self, list_order):
        self._view = PlayerListView()
        self._list_order = list_order

    def __call__(self):
        # Generate the ordered player list
        if self._list_order == "Ranking":
            players_list = self._sort_by_ranking()
        elif self._list_order == "Name":
            players_list = self._sort_by_name()

        # Show the players list
        self._view.show_players(players_list)

        # Return to the Tournaments Reports controller
        return main_controllers.GenerateReportsController()
