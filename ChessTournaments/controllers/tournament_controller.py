from . import main_controllers
from ..views.tournament_view import NewTournamentFormView, StartTournamentView
from ..views.menu_views import (
    NewTournamentStartMenuView,
    NewTournamentMenuView
    )
from ..views.tournament_view import NewTournamentAddPlayerView
from ..models.menus import Menu
from ..models.Player import Players, Player
from ..models.Tournament import Tournaments


class NewTournamentController:
    def __init__(self):
        self.menu = Menu()
        self._view = NewTournamentMenuView(self.menu)

    def __call__(self):
        # 1. Generate the new tournament menu
        self.menu.add(
            "auto",
            "Paramétrer le tournoi",
            NewTournamentFormController())
        self.menu.add(
            "auto",
            "Revenir au menu principal",
            main_controllers.HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # 2. Ask user choice
        user_choice = self._view.get_user_choice()

        # 3. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler


class ChoiceTournamentController:

    def __init__(self):
        pass

    def __call__(self):
        pass


class StartTournamentController:

    def __init__(self, tournament):
        self.menu = Menu()
        self._tournament = tournament
        self._view = StartTournamentView()
        self._turn_menu_view = TurnMenuView(self.menu, tournament.turn_in_progress)

    def __call__(self):
        # 1. Peer generation
        peer_list = self._peer_generation()

        # 2. Show peer for this turn
        self._view.show_peer(peer_list)

        # 3. Ask for match results
        for peer in peer_list:
            tournament = self._set_peer_result(peer, tournament)

        # 4. Update the turn number
        tournament.turn_in_progress += 1

        # 5. Save the tournament
        Tournaments.update_tournament(tournament)

        self.menu.add(
            "s",
            "Lancer le tour suivant",
            StartTournamentController(self.tournament))
        self.menu.add(
            "h",
            "Allez au menu d'acceuil",
            main_controllers.HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # 4. Ask user choice
        user_choice = self._turn_menu_view.get_user_choice()

        # 5. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler

    def _peer_generation(self, tournament):
        if tournament.turn_in_progress == 1:
            pass
        else:
            pass

    def _set_peer_result(self, peer, tournament):
        pass


class NewTournamentFormController:

    def __init__(self):
        self._view = NewTournamentFormView()

    def __call__(self):
        # 1. Ask for tournament setup
        tournament = self._view.get_user_setup()

        # 2. Show tournament summary
        self._view.new_tournament_summary(tournament)

        # 3. Ask user validation
        # (verfication that the tournament has no mistake)
        user_validation = self._view.get_user_validation()
        if not user_validation:
            return main_controllers.HomeMenuController()

        # 4. Save the tournament setup
        Tournaments.add_to_database(tournament)

        # 5. Ask user choice (start tournament / back to main menu)
        return NewTournamentStartController(tournament)


class NewTournamentStartController:

    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self._view = NewTournamentStartMenuView(self.menu)

    def __call__(self):
        # 1. Generate the new tournament start menu
        self.menu.add(
            "auto",
            "Lancer le tournoi",
            StartTournamentController(self.tournament))
        self.menu.add(
            "auto",
            "Revenir au menu principal",
            main_controllers.HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # 2. Ask user choice
        user_choice = self._view.get_user_choice()

        # 3. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler


def new_tournament_add_player_controller():
    _view = NewTournamentAddPlayerView()
    _players_list = []
    numbers_of_players = 0

    while True:
        numbers_of_players += 1
        player_added = False
        # 1. Ask for player name
        name = _view.get_player_name(numbers_of_players)
        if name == "":
            return _players_list

        # 2. Check if this name is already in Players.players list
        players_with_same_name = Players.is_player_exist(name)
        if len(players_with_same_name) > 0:
            # 2.1   There is at least one player with the same name
            # 2.1.1 Ask if one of this(these) player(s) is the player
            #   which participate to these tournament
            player_choice = _view.ask_if_player_in_list(players_with_same_name)
            if player_choice in range(len(players_with_same_name)):
                player_added = True
                player_id = Players.get_player_id(
                    players_with_same_name[player_choice])
                _players_list.append(player_id)

        if not player_added:
            # 2.2   This is a new player, add to the tournament players list
            #       and to the db_players.json
            # 2.2.1 Ask for its firstname
            firstname = _view.get_player_firstname()
            # 2.2.2 Ask for its birthday
            birthday = _view.get_player_birthday()
            # 2.2.3 Ask for its sex
            sex = _view.get_player_sex()
            # 2.2.4 Ask for its rank
            rank = _view.get_player_rank()
            # 2.2.5 Add to the tournament players list and to db_players.json
            player = Player(name, firstname, birthday, sex, rank)
            _players_list.append(Players.add_player(player))
