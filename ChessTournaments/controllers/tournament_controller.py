'''Controller link to tournament management.

Classes:
    NewTournamentController
    NewTournamentFormController
    NewTournamentStartController
    ChoiceTournamentController
    StartTournamentController
    TournamentListController
    GenerateTournamentsReportsController
    TournamentsReportsListController

Functions:
    new_tournament_add_player_controller

'''

from datetime import date

from . import main_controllers
from ..views.tournament_view import (
    NewTournamentFormView,
    StartTournamentView,
    NewTournamentAddPlayerView,
    TournamentListView,
    TournamentResultView,
    TournamentsReportsListView
    )
from ..views.menu_views import (
    NewTournamentStartMenuView,
    NewTournamentMenuView,
    TurnMenuView,
    ChoiceTournamentMenuView,
    TournamentTerminatedMenuView,
    GenerateReportsMenuView
    )
from ..models.menus import Menu
from ..models.Player import Players, Player
from ..models.Tournament import Tournaments


class NewTournamentController:
    '''Controller which ask for the creation of a new tournament

    The user can also go back to home menu or quit the application.

    '''

    def __init__(self):
        self._menu = Menu()
        self._view = NewTournamentMenuView(self._menu)

    def __call__(self):
        # Generate the new tournament menu
        self._menu.add(
            "auto",
            "Paramétrer le tournoi",
            NewTournamentFormController())
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


class NewTournamentFormController:
    '''Controller link to NewTournamentController.
    Aim to create a new tournament.
    '''

    def __init__(self):
        self._view = NewTournamentFormView()

    def __call__(self):
        # Ask for tournament setup
        tournament = self._view.get_user_setup()

        # Show tournament summary
        self._view.new_tournament_summary(tournament)

        # Ask user validation
        # (verfication that the tournament has no mistake)
        user_validation = self._view.get_user_validation()
        if not user_validation:
            return main_controllers.HomeMenuController()

        # Save the tournament setup
        Tournaments.add_tournament(tournament)

        # Ask user choice (start tournament / back to main menu)
        return NewTournamentStartController(tournament)


def new_tournament_add_player_controller():
    '''Controller used to simplify adding new players in a tournament.'''

    _view = NewTournamentAddPlayerView()
    _players_list = []
    numbers_of_players = 0

    while True:
        numbers_of_players += 1
        player_added = False
        # Ask for player name
        name = _view.get_player_name(numbers_of_players)
        if name == "":
            return _players_list

        # Check if this name is already in Players.players list
        players_with_same_name = Players.is_player_exist(name)
        if len(players_with_same_name) > 0:
            # There is at least one player with the same name
            #   Ask if one of this(these) player(s) is the player
            #   which participate to these tournament
            player_choice = _view.ask_if_player_in_list(players_with_same_name)
            if player_choice in range(len(players_with_same_name)):
                player_added = True
                player_id = Players.get_player_id(
                    players_with_same_name[player_choice])
                _players_list.append(player_id)

        if not player_added:
            # This is a new player, add to the tournament players list
            # and to the db_players.json
            #   Ask for its firstname
            firstname = _view.get_player_firstname()
            #   Ask for its birthday
            birthday = _view.get_player_birthday()
            #   Ask for its sex
            sex = _view.get_player_sex()
            #   Ask for its rank
            rank = _view.get_player_rank()
            #   Add to the tournament players list and to db_players.json
            player = Player(name, firstname, birthday, sex, rank)
            _players_list.append(Players.add_player(player))


class NewTournamentStartController:
    '''Controller link to NewTournamentFormController.

    When the tournament is created, ask to the user if he want to:
        Start the tournament
        Go back to home menu
        Quit the application

    '''

    def __init__(self, tournament):
        self._tournament = tournament
        self._menu = Menu()
        self._view = NewTournamentStartMenuView(self._menu)

    def __call__(self):
        # Generate the new tournament start menu
        self._menu.add(
            "auto",
            "Lancer le tournoi",
            StartTournamentController(self._tournament))
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


class ChoiceTournamentController:
    '''Controller used to let the user choice a tournament.

    Let the user choose of the kind of display :
        All tournament (sorted or not)
        Tournament not yet finished

    The user can also go back to home menu or quit the application.

    '''

    def __init__(self):
        self._menu = Menu()
        self._view = ChoiceTournamentMenuView(self._menu)

    def __call__(self):
        # Generate the choice tournament menu
        self._menu.add(
            "auto",
            "Afficher la liste des tournois",
            TournamentListController())
        self._menu.add(
            "auto",
            "Afficher la liste des tournois en cours",
            TournamentListController("In_Progress"))
        self._menu.add(
            "auto",
            "Afficher la liste des tournois par nom",
            TournamentListController("Name"))
        self._menu.add(
            "auto",
            "Afficher la liste des tournois par lieu",
            TournamentListController("Location"))
        self._menu.add(
            "auto",
            "Afficher la liste des tournois par date",
            TournamentListController("Date"))
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


class StartTournamentController:
    '''Controller which manage a tournament.

    Check if the tournament is not over.
    Then generate the list of peer of the turn in progress.
    Ask, for each peer, the match result.
    Update the tournament in database.
    Ask to the user if the tournament continu or
    if he want to go back to home menu or quit the application.

    '''

    def __init__(self, tournament):
        self._menu = Menu()
        self._tournament = tournament
        self._view = StartTournamentView()
        self._view_result = TournamentResultView()

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
            self._menu, self._tournament.turn_in_progress)
        self._menu.add(
            "auto",
            "Lancer ce tour",
            StartTournamentController(self._tournament))
        self._menu.add(
            "a",
            "Allez au menu d'acceuil",
            main_controllers.HomeMenuController())
        self._menu.add(
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
            "a",
            "Allez au menu d'acceuil",
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


class TournamentListController:
    '''Controller linked to ChoiceTournamentController that
    aim to show a sorted or filtering list of tournament
    and let the user choose between the following choice:
        Start the choosen tournament
        Go back to home menu
        Quit the application

    '''

    def __init__(self, list_filter=None):
        self._menu = Menu()
        self._menu_view = ChoiceTournamentMenuView(self._menu)
        self._view = TournamentListView()
        if list_filter == "In_Progress":
            self._tournaments_list = self._tournaments_in_progress()
        elif list_filter == "Name":
            self._tournaments_list = self._sort_by_name()
        elif list_filter == "Location":
            self._tournaments_list = self._sort_by_location()
        elif list_filter == "Date":
            self._tournaments_list = self._sort_by_date()
        else:
            self._tournaments_list = Tournaments.tournaments

    def __call__(self):
        # Show the tournaments list
        self._view.show_tournaments(self._tournaments_list)

        # Ask tournament choice
        choice = self._view.get_tournament_choice()

        # Generate the tournament start menu
        self._menu.add(
            "auto",
            f"Lancer le tournoi n°{choice + 1}",
            StartTournamentController(self._tournaments_list[choice]))
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


class GenerateTournamentsReportsController:
    '''Controller link to GenerateReportsController that aim
    to let the user to choose reports link to tournament'''

    def __init__(self, tournament_number=None):
        self._menu = Menu()
        self._view_tournament = TournamentListView()
        self._view_report = GenerateReportsMenuView(self._menu)
        self._tournament_number = tournament_number

    def __call__(self):
        if self._tournament_number is None:
            # Show the tournament list
            self._view_tournament.show_tournaments(Tournaments.tournaments)

            # Ask tournament choice
            choice = self._view_tournament.get_tournament_choice()
        else:
            choice = self._tournament_number

        # Generate the reports menu
        self._menu.add(
            "auto",
            "Afficher tous les joueurs du tournoi "
            f"n°{choice + 1} par ordre alphabétique",
            TournamentsReportsListController(
                Tournaments.tournaments[choice],
                "Name",
                choice))
        self._menu.add(
            "auto",
            "Afficher tous les joueurs du tournoi "
            f"n°{choice + 1} par classement",
            TournamentsReportsListController(
                Tournaments.tournaments[choice],
                "Ranking",
                choice))
        self._menu.add(
            "auto",
            f"Afficher tous les tours du tournoi n°{choice + 1}.",
            TournamentsReportsListController(
                Tournaments.tournaments[choice],
                "Turn",
                choice))
        self._menu.add(
            "auto",
            f"Afficher tous les matchs du tournoi n°{choice + 1}",
            TournamentsReportsListController(
                Tournaments.tournaments[choice],
                "Match",
                choice))
        self._menu.add(
            "auto",
            "Revenir à la liste des rapports",
            main_controllers.GenerateReportsController())
        self._menu.add(
            "a",
            "Allez au menu d'acceuil",
            main_controllers.HomeMenuController())
        self._menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # Ask user choice
        user_choice = self._view_report.get_user_choice()

        # Return the controller link to user choice
        # to the main controller
        return user_choice.handler


class TournamentsReportsListController:
    '''Controller link to GenerateTournamentsReportsController
    that aim to show the choosen tournament report then let the
    user choose another kind of report about this tournament,
    or go back to the list of all kind of report,
    or to go back to home menu,
    or to quit the application.

    '''

    def __init__(self, tournament, list_filter, choice):
        self._view = TournamentsReportsListView()
        self._list_filter = list_filter
        if list_filter == "Name":
            self._tournament_report = self._sort_player_by_name(tournament)
        elif list_filter == "Ranking":
            self._tournament_report = self._sort_player_by_ranking(tournament)
        elif list_filter == "Turn" or list_filter == "Match":
            self._tournament_report = tournament.turns
        self._choice = choice

    def __call__(self):
        # Show the tournament report
        self._view.show_report(self._tournament_report, self._list_filter)

        # Return to the Tournaments Reports controller
        return GenerateTournamentsReportsController(self._choice)

    def _sort_player_by_name(self, tournament):
        players = []
        for player_id in tournament.players:
            players.append(Players.get_player_by_id(player_id))
        players.sort(key=lambda x: (x.name, x.firstname))
        return players

    def _sort_player_by_ranking(self, tournament):
        players = []
        for player_id in tournament.players:
            players.append(Players.get_player_by_id(player_id))
        players.sort(reverse=True)
        return players
