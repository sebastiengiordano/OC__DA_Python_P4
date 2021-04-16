from datetime import date

from . import main_controllers
from ..views.tournament_view import (
    NewTournamentFormView,
    StartTournamentView,
    NewTournamentAddPlayerView,
    TournamentListView,
    TournamentResult
    )
from ..views.menu_views import (
    NewTournamentStartMenuView,
    NewTournamentMenuView,
    TurnMenuView,
    ChoiceTournamentMenuView,
    TournamentTerminatedMenuView
    )
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
        self.menu = Menu()
        self._view = ChoiceTournamentMenuView(self.menu)

    def __call__(self):
        # 1. Generate the choice tournament menu
        self.menu.add(
            "auto",
            "Afficher la liste des tournois",
            TournamentListController())
        self.menu.add(
            "auto",
            "Afficher la liste des tournois en cours",
            TournamentListController("In_Progress"))
        self.menu.add(
            "auto",
            "Afficher la liste des tournois par nom",
            TournamentListController("Name"))
        self.menu.add(
            "auto",
            "Afficher la liste des tournois par lieu",
            TournamentListController("Location"))
        self.menu.add(
            "auto",
            "Afficher la liste des tournois par date",
            TournamentListController("Date"))
        self.menu.add(
            "a",
            "Allez au menu d'acceuil",
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


class StartTournamentController:
    '''
    '''
    def __init__(self, tournament):
        self.menu = Menu()
        self._tournament = tournament
        self._view = StartTournamentView()
        self._view_result = TournamentResult()

    def __call__(self):
        # Tournament terminated
        numbers_of_turns = self._tournament.numbers_of_turns
        if self._tournament.turn_in_progress > numbers_of_turns:
            return self._tournament_terminated()

        while True:
            # Peer generation
            peer_list = self._peer_generation(self._tournament)

            # Show peer for this turn
            self._view.show_peer(peer_list, self._tournament.turn_in_progress)

            # Ask for match results
            results = []
            # Update results
            for peer in peer_list:
                if peer[1] == "":
                    results.append((1, 0))
                else:
                    results.append(self._view.ask_4_result((peer)))
            # Ask for results validation
            if self._view.get_user_validation(
                    peer_list, results, self._tournament.turn_in_progress):
                # Save these results
                self._tournament.save_peers_results(
                    peer_list, results)

                # Update the turn number
                self._tournament.turn_in_progress += 1
                # If tournament is terminated
                if self._tournament.turn_in_progress > numbers_of_turns:
                    # Update the end date
                    self._tournament.end_date = date.today()
                    # Save the tournament
                    Tournaments.update_tournament(self._tournament)
                    # Show the tournament result
                    self._view_result.show_tournament_result(self._tournament)
                    # Go to Tournament terminated menu
                    return self._tournament_terminated()

                # Save the tournament
                Tournaments.update_tournament(self._tournament)

            # Generate the turn menu
            self._turn_menu_generation()

            # Ask user choice
            user_choice = self._turn_menu_view.get_user_choice()

            # Return the controller link to user choice
            # to the main controller
            return user_choice.handler

    def _peer_generation(self, tournament):
        # First turn
        if tournament.turn_in_progress == 1:
            return self._peer_generation_first_turn(tournament)
        # Next turns
        else:
            return self._peer_generation_others_turns(tournament)

    def _peer_generation_first_turn(self, tournament):
        players_list = []
        peer = []
        # Sort all players based on their rank.
        for player_id in tournament.players:
            players_list.append(Players.get_player_by_id(player_id))
        players_list.sort(reverse=True)
        # Divide the players into two halves
        number_of_peer = len(players_list) // 2
        odd_number_of_players = len(players_list) % 2
        for index in range(number_of_peer):
            peer.append(
                (players_list[index], players_list[index + number_of_peer]))
        if odd_number_of_players:
            peer.append((players_list[-1], ""))
        return peer

    def _peer_generation_others_turns(self, tournament):
        players_list = []
        peer = []
        # Sort all the players according to their total number of points.
        # If several players have the same number of points,
        # sort them according to their rank.
        tournament.update_scores()
        for player_id in tournament.players:
            player = Players.get_player_by_id(player_id)
            player_score = tournament.get_player_score(player)
            players_list.append((player, player_score))
        players_list.sort(key=lambda x: (x[1], x[0]), reverse=True)

        tournament.update_players_opponent()
        # Match player 1 with player 2, player 3 with player 4, and so on.
        # If these players have already played together before,
        # pair them with following player.
        while len(players_list) > 0:
            player_1_score = players_list.pop(0)
            opponent_find = False
            player_1_id = Players.get_player_id(player_1_score[0])
            players_opponent = tournament.get_players_opponent(player_1_id)
            for player_2_score in players_list:
                player_2_id = Players.get_player_id(player_2_score[0])
                if player_2_id not in players_opponent:
                    peer.append((player_1_score[0], player_2_score[0]))
                    players_list.remove(player_2_score)
                    opponent_find = True
                    break
            if not opponent_find:
                peer.append((player_1_score[0], ""))
        return peer

    def _turn_menu_generation(self):
        self._turn_menu_view = TurnMenuView(
            self.menu, self._tournament.turn_in_progress)
        self.menu.add(
            "auto",
            "Lancer ce tour",
            StartTournamentController(self._tournament))
        self.menu.add(
            "auto",
            "Revenir au menu principal",
            main_controllers.HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

    def _tournament_terminated(self):
        menu = Menu()
        tournament_terminated_view = TournamentTerminatedMenuView(menu)
        menu.add(
            "auto",
            "Lancer / Reprendre un tournoi",
            ChoiceTournamentController())
        menu.add(
            "auto",
            "Revenir au menu principal",
            main_controllers.HomeMenuController())
        menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # Ask user choice
        user_choice = tournament_terminated_view.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
        return user_choice.handler


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
        Tournaments.add_tournament(tournament)

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


class TournamentListController:

    def __init__(self, list_filter=None):
        self.menu = Menu()
        self._menu_view = ChoiceTournamentMenuView(self.menu)
        self._view = TournamentListView()
        if list_filter == "In_Progress":
            self.tournaments_list = self._tournaments_in_progress()
        elif list_filter == "Name":
            self.tournaments_list = self._sort_by_name()
        elif list_filter == "Location":
            self.tournaments_list = self._sort_by_location()
        elif list_filter == "Date":
            self.tournaments_list = self._sort_by_date()
        else:
            self.tournaments_list = Tournaments.tournaments

    def __call__(self):
        # 1. Show the tournaments list
        self._view.show_tournaments(self.tournaments_list)

        # 2. Ask tournament choice
        choice = self._view.get_tournament_choice()

        # 3. Generate the tournament start menu
        self.menu.add(
            "auto",
            f"Lancer le tournoi n°{choice + 1}",
            StartTournamentController(self.tournaments_list[choice]))
        self.menu.add(
            "auto",
            "Revenir au menu principal",
            main_controllers.HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # 4. Ask user choice
        user_choice = self._menu_view.get_user_choice()

        # 5. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler

    def _tournaments_in_progress(self):
        tournaments_list = []
        for tournament in Tournaments.tournaments:
            if tournament.turn_in_progress <= tournament.numbers_of_turns:
                tournaments_list.append(tournament)
        return tournaments_list

    def _sort_by_name(self):
        tournaments_list = []
        for index, tournament in enumerate(Tournaments.tournaments):
            insert_tournament = False
            if index == 0:
                tournaments_list.append(tournament)
            else:
                enum = enumerate(tournaments_list)
                for index_list, tournament_in_list in enum:
                    if tournament_in_list.name > tournament.name:
                        tournaments_list.insert(index_list, tournament)
                        insert_tournament = True
                        break
                if not insert_tournament:
                    tournaments_list.append(tournament)
        return tournaments_list

    def _sort_by_location(self):
        tournaments_list = []
        for index, tournament in enumerate(Tournaments.tournaments):
            insert_tournament = False
            if index == 0:
                tournaments_list.append(tournament)
            else:
                enum = enumerate(tournaments_list)
                for index_list, tournament_in_list in enum:
                    if tournament_in_list.location > tournament.location:
                        tournaments_list.insert(index_list, tournament)
                        insert_tournament = True
                        break
                if not insert_tournament:
                    tournaments_list.append(tournament)
        return tournaments_list

    def _sort_by_date(self):
        tournaments_list = []
        for index, tournament in enumerate(Tournaments.tournaments):
            insert_tournament = False
            if index == 0:
                tournaments_list.append(tournament)
            else:
                enum = enumerate(tournaments_list)
                for index_list, tournament_in_list in enum:
                    if tournament_in_list.start_date > tournament.start_date:
                        tournaments_list.insert(index_list, tournament)
                        insert_tournament = True
                        break
                if not insert_tournament:
                    tournaments_list.append(tournament)
        return tournaments_list
