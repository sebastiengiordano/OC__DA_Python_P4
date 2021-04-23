'''View link to tournament management.

Classes:
    NewTournamentFormView
    StartTournamentView
    NewTournamentAddPlayerView
    TournamentListView
    TournamentResultView
    TournamentsReportsListView

'''

import datetime

from . import view_utils
from .views_parameters import (
    text_left_side_offset_view,
    first_indent_view,
    input_label,
    MENU_LEFT_SIDE_OFFSET,
    TEXT_LEFT_SIDE_OFFSET,
    DESCRIPTION_DISPLAY_MAX_SIZE,
    FIRST_INDENT
    )
from ..models import Tournament
from ..models.Player import Players
from ..tools.tools_utils import (
    is_date_format,
    datetime_to_str,
    valid_name
    )
from ..controllers import tournament_controller


class NewTournamentFormView:
    '''Form used to create a new chess tournament.'''

    def get_user_setup(self):
        tournament = Tournament.Tournament()

        # Ask for the tournament setup
        print("\n Veuillez indiquer :")

        # Ask for the tournament name
        tournament.name = self._ask_4_tournament_name()

        # Ask for the tournament location
        tournament.location = self._ask_4_tournament_location()

        # Ask for the tournament date
        tournament.start_date = self._ask_4_tournament_date()
        tournament.end_date = tournament.start_date

        # Ask for the numbers of turns
        tournament.numbers_of_turns = self._ask_4_numbers_of_turns(tournament)

        # Ask for names of participants
        tournament.players = self._ask_4_names_of_participants()

        # Ask for time control type
        tournament.time_control = self._ask_4_time_control_type(tournament)

        # Ask for the tournament description
        tournament.description = input(
            "\n" + text_left_side_offset_view
            + "- la description du tournoi\n"
            + input_label)

        return tournament

    def get_user_validation(self):
        while True:
            print(
                "\n Est-ce que les informations sur ce tournoi"
                "sont correctes ? (o/n)")
            user_input = input(input_label)
            if user_input == "":
                pass
            elif user_input in "oO":
                return True
            elif user_input in "nN":
                return False

            print("\n /** Veuillez entrer o pour oui, **\\", end="")
            print("\n /**                 n pour non. **\\")

    def new_tournament_summary(self, tournament):
        max_lenght = self.max_lenght(tournament)
        menu_frame, menu_label = view_utils.menu_frame_design(
            "Résumé du tournoi",
            max_lenght)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        print(
            text_left_side_offset_view
            + f"Nom  : {tournament.name}")
        print(
            text_left_side_offset_view
            + f"Lieu : {tournament.location}")
        self._show_tournament_date(tournament)
        print(
            text_left_side_offset_view
            + f"Nombre de tours : {tournament.numbers_of_turns}")
        self._show_tournament_players(tournament, max_lenght)
        print(
            text_left_side_offset_view
            + f"Contrôle du temps : {tournament.time_control}")
        self._show_tournament_description(tournament, max_lenght)
        print(menu_frame)

    def max_lenght(self, tournament):
        max_lenght = []
        if len(tournament.description) \
                > DESCRIPTION_DISPLAY_MAX_SIZE:
            max_lenght.append(DESCRIPTION_DISPLAY_MAX_SIZE)
        max_lenght.append(
            len(tournament.name)
            + len("Nom : ")
            + TEXT_LEFT_SIDE_OFFSET
            )
        max_lenght.append(
            len(tournament.location)
            + len("Lieu : ")
            + TEXT_LEFT_SIDE_OFFSET
            )
        for player_id in tournament.players:
            player = Players.get_player_by_id(player_id)
            max_lenght.append(
                len(player)
                + TEXT_LEFT_SIDE_OFFSET
                )
        max_lenght.append(
            len("Contrôle du temps : ")
            + len(tournament.time_control)
            + TEXT_LEFT_SIDE_OFFSET
            )
        max_lenght.sort()
        return max_lenght[-1]

    def _ask_4_tournament_name(self):
        while True:
            name = input(
                text_left_side_offset_view
                + "- le nom du tournoi\n"
                + input_label)
            if not(name == ""):
                return name

    def _ask_4_tournament_location(self):
        while True:
            location = input(
                "\n" + text_left_side_offset_view
                + "- le lieu\n"
                + input_label)
            if not(location == ""):
                return location

    def _ask_4_tournament_date(self):
        while True:
            date = input(
                "\n" + text_left_side_offset_view
                + "- la date (au format jj/mm/aaaa)\n"
                + text_left_side_offset_view + first_indent_view
                + "(appuyer sur la touche \"Entrée\" sans renseigner"
                + "\n" + text_left_side_offset_view + first_indent_view
                + " de valeur pour choisir la date d'aujourd'hui.\n)"
                + input_label)
            if date == "":
                return datetime.date.today()
            else:
                date = is_date_format(date)
                if isinstance(date, datetime.date):
                    if date < date.today():
                        view_utils.alert_message_centered(
                            " Attention,",
                            "Vous avez mentionné",
                            " une date dans le passé.")
                    if date > date.today():
                        view_utils.alert_message_centered(
                            " Attention,",
                            "Vous avez mentionné",
                            " une date dans le futur.")
                    return date
                elif date:
                    if date == "day is out of range for month":
                        view_utils.alert_message_centered(
                            "Format de date invalide.",
                            "Le jour indiqué est trop",
                            "grand pour ce mois-ci.")
                    elif date == "month must be in 1..12":
                        view_utils.alert_message_centered(
                            "Format de date invalide.",
                            "Le mois doit être compris",
                            "entre 1 et 12.")
                else:
                    print("\n /** Format de date invalide. **\\")
                print("\n Veuillez indiquer :", end="")

    def _ask_4_numbers_of_turns(self, tournament):
        while True:
            print(
                "\n    - le nombre de tours ("
                f"{tournament.numbers_of_turns} par défaut)\n"
                + text_left_side_offset_view + first_indent_view
                + "(appuyer sur la touche \"Entrée\" sans renseigner"
                + "\n" + text_left_side_offset_view + first_indent_view
                + " de valeur pour choisir la valeur par défaut.)")
            user_input = input(input_label)
            if user_input == "":
                return tournament.numbers_of_turns
            try:
                user_input = int(user_input)
                return user_input
            except Exception:
                view_utils.alert_message_centered(
                    "Format invalide.",
                    " Veuillez choisir un",
                    " nombre entier.")
                print("\n Veuillez indiquer :", end="")

    def _ask_4_names_of_participants(self):
        print("\n" + text_left_side_offset_view + "- la liste des joueurs")
        print(
            text_left_side_offset_view + first_indent_view
            + "(appuyer sur la touche \"Entrée\" sans renseigner"
            + "\n" + text_left_side_offset_view + first_indent_view
            + " de nom pour terminer cette étape.)",
            end="")
        return tournament_controller.new_tournament_add_player_controller()

    def _ask_4_time_control_type(self, tournament):
        while True:
            print(
                "\n" + text_left_side_offset_view
                + "- le type de contrôle de temps")
            for key, value in tournament.time_control_type.items():
                print(
                    text_left_side_offset_view * 2
                    + f"{key} : {value}")
            time_control = input(input_label)
            if time_control in tournament.time_control_type:
                return tournament.time_control_type[time_control]
            else:
                print("\n /** Veuillez entrer 1, 2 ou 3. **\\")
            print("\n Veuillez indiquer :", end="")

    def _show_tournament_date(self, tournament):
        print(
            text_left_side_offset_view
            + f"Date : {tournament.start_date:%d}/"
            + f"{tournament.start_date:%m}/"
            + f"{tournament.start_date:%Y}")

    def _show_tournament_players(self, tournament, max_lenght):
        print(text_left_side_offset_view + "Liste des joueurs :")
        for player_id in tournament.players:
            player = Players.get_player_by_id(player_id)
            player = player.name + " " + player.firstname
            print(
                " " * MENU_LEFT_SIDE_OFFSET
                + player.center(
                    max_lenght
                    + TEXT_LEFT_SIDE_OFFSET))

    def _show_tournament_description(self, tournament, max_lenght):
        print(text_left_side_offset_view + "Description :")
        if not tournament.description == "":
            description = tournament.description.split()
            description_display_size = (
                max_lenght
                + TEXT_LEFT_SIDE_OFFSET
                - MENU_LEFT_SIDE_OFFSET)
            size = (
                TEXT_LEFT_SIDE_OFFSET
                + FIRST_INDENT)
            print(" " * size, end="")
            for text in description:
                if size + len(text) < description_display_size:
                    text = text + " "
                    print(text, end="")
                    size += len(text)
                else:
                    text = "\n    " + text + " "
                    print(text, end="")
                    size = len(text)
            print("")


class StartTournamentView:
    '''View used for manage a tournament.'''

    def show_peer(self, peer_list, turn_number):
        width = self._peers_lenght(peer_list)

        menu_frame, menu_label = view_utils.menu_frame_design(
            f"\nListe des pairs pour le tour n°{turn_number}",
            width)
        width = max(len(menu_frame), width)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        for player_1, player_2 in peer_list:
            player_one = (
                f"{player_1.name} {player_1.firstname} ("
                + datetime_to_str(player_1.birthday) + ")")
            if not player_2 == "":
                player_two = (
                    f"{player_2.name} {player_2.firstname} ("
                    + datetime_to_str(player_2.birthday) + ")")
                print(
                    "\n" + player_one.center(width)
                    + "\n" + "VS".center(width)
                    + "\n" + player_two.center(width)
                    + "\n"
                    )
            else:
                print(
                    "\n" + player_one.center(width)
                    + "\n" +
                    "ne joue pas ce tour-ci.".center(width)
                    )

        print(menu_frame)

    def ask_4_result(self, peer):
        width = self._peers_lenght((peer,)) + len(" 1 :  gagne")
        while True:
            menu_frame, menu_label = view_utils.menu_frame_design(
                "Résultat du match",
                width)
            print("\n\n" + menu_frame)
            print(menu_label)
            print(menu_frame)
            for player_1, player_2 in (peer,):
                player_one = (
                    f"{player_1.name} {player_1.firstname} ("
                    + datetime_to_str(player_1.birthday) + ")")
                player_two = (
                    f"{player_2.name} {player_2.firstname} ("
                    + datetime_to_str(player_2.birthday) + ")")
                print(
                    player_one.center(width)
                    + "\n" + "VS".center(width)
                    + "\n" + player_two.center(width)
                    )
            print(menu_frame)
            print(
                f" 1 : {player_1.name} {player_1.firstname} ("
                + datetime_to_str(player_1.birthday) + ")"
                + " gagne\n"
                f" 2 : {player_2.name} {player_2.firstname} ("
                + datetime_to_str(player_2.birthday) + ")"
                + " gagne\n"
                " 3 : Egalité"
            )
            print(menu_frame)
            user_input = input(input_label)
            if user_input == "1":
                return (1, 0)
            elif user_input == "2":
                return (0, 1)
            elif user_input == "3":
                return (0.5, 0.5)

    def get_user_validation(self, peer_list, results, turn_number):
        while True:
            self._show_peers_results(peer_list, results, turn_number)
            print(
                "\n Est-ce que les informations sur ce tour "
                "sont correctes ? (o/n)")
            user_input = input(input_label)
            if user_input == "":
                pass
            elif user_input in "oO":
                return True
            elif user_input in "nN":
                return False

            print("\n /** Veuillez entrer o pour oui, **\\", end="")
            print("\n /**                 n pour non. **\\")

    def _show_peers_results(self, peer_list, results, turn_number):
        width = self._peers_lenght(peer_list)
        menu_frame, menu_label = view_utils.menu_frame_design(
            f"Résultat des matchs du tour n°{turn_number}",
            width)
        width = max(len(menu_frame), width)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        for (player_1, player_2), (r1, r2) in zip(peer_list, results):
            player_one = (
                f"{player_1.name} {player_1.firstname} ("
                + datetime_to_str(player_1.birthday) + ")")
            if not player_2 == "":
                player_two = (
                    f"{player_2.name} {player_2.firstname} ("
                    + datetime_to_str(player_2.birthday) + ")")
            if r2 == 0.5:
                print(
                    "\n" + player_one.center(width)
                    + "\n" + "VS".center(width)
                    + "\n" + player_two.center(width)
                )
                print("Egalité".center(width))
            elif r1 == 1:
                print("\n" + player_one.center(width))
                print("gagne".center(width))
            else:
                print("\n" + player_two.center(width))
                print("gagne".center(width))
            print()
        print(menu_frame, end="\n\n")

    def _peers_lenght(self, peer):
        width = 0
        for player_1, player_2 in peer:
            width_1 = len(
                f"{player_1.name} {player_1.firstname} ("
                + datetime_to_str(player_1.birthday) + ")") + 2
            width = max(width_1, width)
            if not player_2 == "":
                width_2 = len(
                    f"{player_2.name} {player_2.firstname} ("
                    + datetime_to_str(player_2.birthday) + ")") + 2
                width = max(width_2, width)
        return width


class NewTournamentAddPlayerView:
    '''View used when the user want to add a new player.'''

    def get_player_name(self, numbers_of_players):
        while True:
            print(
                "\n" + text_left_side_offset_view
                + f"- le nom du joueur {numbers_of_players}")
            player_name = input("   " + input_label)
            if not valid_name(player_name):
                view_utils.alert_message_centered(
                    "Format invalide.",
                    "Le nom ne doit être",
                    "composé que de lettre.")
            else:
                return player_name.capitalize()

    def get_player_firstname(self):
        print(
            "\n" + text_left_side_offset_view
            + "- le prénom du joueur")
        player_firstname = input("   " + input_label)
        if not valid_name(player_firstname):
            view_utils.alert_message_centered(
                "Format invalide.",
                "Le prénom ne doit être",
                "composé que de lettre.")
        else:
            return player_firstname.capitalize()

    def get_player_birthday(self):
        while True:
            birthday = input(
                "\n" + text_left_side_offset_view
                + "-sa date d'anniversaire (au format jj/mm/aaaa)\n"
                + input_label)
            birthday = is_date_format(birthday)
            if isinstance(birthday, datetime.date):
                return birthday
            elif birthday:
                if birthday == "day is out of range for month":
                    view_utils.alert_message_centered(
                        "Format de date invalide.",
                        "Le jour indiqué est trop",
                        "grand pour ce mois-ci.")
                elif birthday == "month must be in 1..12":
                    view_utils.alert_message_centered(
                        "Format de date invalide.",
                        "Le mois doit être compris",
                        "entre 1 et 12.")
            else:
                print("\n /** Format de date invalide. **\\")
            print("\n Veuillez indiquer :", end="")

    def get_player_sex(self):
        while True:
            sex = input(
                "\n" + text_left_side_offset_view
                + "- le sexe du joueur (M/F)\n"
                + input_label)
            if sex != "" and sex in "mfMF":
                return sex.upper()
            else:
                print("\n /** Réponse invalide. **\\")
            print("\n Veuillez indiquer :", end="")

    def get_player_rank(self):
        while True:
            rank = input(
                "\n" + text_left_side_offset_view
                + "- le classement du joueur\n"
                + text_left_side_offset_view + first_indent_view
                + "(appuyer sur la touche \"Entrée\" sans renseigner"
                + "\n" + text_left_side_offset_view + first_indent_view
                + " de valeur pour choisir la valeur 0.)\n"
                + input_label)
            if rank.isdigit():
                return int(rank)
            elif rank == "":
                return 0
            else:
                print("\n /** Réponse invalide. **\\")
            print("\n Veuillez indiquer :", end="")

    def ask_if_player_in_list(self, players):
        while True:
            player_number = 0
            size_list = [len(player) for player in players]
            size_list.sort()
            max_lenght = size_list[-1]
            menu_frame, menu_label = view_utils.menu_frame_design(
                "Liste des joueurs portant le même nom",
                max_lenght)
            print("\n" + menu_frame)
            print(menu_label)
            print(menu_frame, end='')
            for player in players:
                player_number += 1
                print(
                    "\n" + text_left_side_offset_view
                    + f"Joueur n°{player_number}:\n"
                    + text_left_side_offset_view
                    + f"   Nom: {player.name}\n"
                    + text_left_side_offset_view
                    + f"   Prénom: {player.firstname}\n"
                    + text_left_side_offset_view
                    + "   Date de naissance: "
                    + datetime_to_str(player.birthday)
                    + "\n"
                    + text_left_side_offset_view
                    + f"   Sexe: {player.sex}")
            print(menu_frame)
            print(
                text_left_side_offset_view
                + "Veuillez indiquer le numéro du joueur:\n"
                + text_left_side_offset_view + first_indent_view
                + "(appuyer sur la touche \"Entrée\" sans renseigner"
                + "\n" + text_left_side_offset_view + first_indent_view
                + " de valeur si aucun joueur ne correspond.)")
            player_choice = input("   " + input_label)
            if player_choice == "":
                return None
            elif (
                    player_choice.isdigit()
                    and int(player_choice) in range(1, len(players) + 1)):
                return int(player_choice) - 1


class TournamentListView(NewTournamentFormView):
    '''View used to show a list of tournament and
    allow the user to choose one of them.'''

    def show_tournaments(self, tournaments_list):
        self.number = 0
        for tournament in tournaments_list:
            self.number += 1
            self._tournament_summary(tournament, self.number)

    def get_tournament_choice(self):
        choice_list = [str(i) for i in range(1, self.number + 1)]
        while True:
            # Ask the user its choice
            print(
                "\nVeuillez indiquer le numéro du tournoi choisi.")
            choice = input(input_label)
            # Validate the user choice
            if choice in choice_list:
                # Return the user choice
                return int(choice) - 1

    def _tournament_summary(self, tournament, number):
        max_lenght = self.max_lenght(tournament)
        menu_frame, menu_label = view_utils.menu_frame_design(
            f"Résumé du tournoi n°{number}",
            max_lenght)
        print("\n\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        print(
            text_left_side_offset_view
            + f"Nom  : {tournament.name}")
        print(
            text_left_side_offset_view
            + f"Lieu : {tournament.location}")
        self._show_tournament_date(tournament)
        print(
            text_left_side_offset_view
            + f"Nombre de tours : {tournament.numbers_of_turns}")
        if tournament.turn_in_progress <= tournament.numbers_of_turns:
            print(
                text_left_side_offset_view
                + f"Tours en cours : {tournament.turn_in_progress}")
        else:
            print(
                " " * MENU_LEFT_SIDE_OFFSET
                + "Tournoi terminé".center(len(menu_frame)))
        self._show_tournament_players(tournament, max_lenght)
        print(
            text_left_side_offset_view
            + f"Contrôle du temps : {tournament.time_control}")
        self._show_tournament_description(tournament, max_lenght)
        print(menu_frame)


class TournamentResultView(NewTournamentFormView):
    '''View used to show the result of a tournament
    when it has just finished.'''

    def show_tournament_result(self, tournament):
        max_lenght = self.max_lenght(tournament)
        menu_frame, menu_label = view_utils.menu_frame_design(
            "Résultat du tournoi",
            max_lenght)
        max_lenght = max(max_lenght, len(menu_frame))
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        print(
            text_left_side_offset_view
            + f"Nom  : {tournament.name}")
        print(
            text_left_side_offset_view
            + f"Lieu : {tournament.location}")
        self._show_tournament_date(tournament)
        print(
            text_left_side_offset_view
            + f"Nombre de tours : {tournament.numbers_of_turns}")
        if tournament.turn_in_progress <= tournament.numbers_of_turns:
            print(
                text_left_side_offset_view
                + f"Tours en cours : {tournament.turn_in_progress}")
        else:
            print("Tournoi terminé".center(len(menu_frame)))
        self._show_tournament_score(tournament, max_lenght)
        print(
            text_left_side_offset_view
            + f"Contrôle du temps : {tournament.time_control}")
        self._show_tournament_description(tournament, max_lenght)
        print(menu_frame)

    def _show_tournament_score(self, tournament, max_lenght):
        tournament.update_scores()
        print("\n" + text_left_side_offset_view + "Classement des joueurs :")
        players_list = self._sort_by_score(tournament)
        for player, score in players_list:
            score = view_utils.score_padding(score)
            player = (
                player.name
                + " "
                + player.firstname
                + " ("
                + datetime_to_str(player.birthday)
                + ")")
            print(
                text_left_side_offset_view
                + first_indent_view
                + player
                + score.rjust(
                    max_lenght
                    - len(
                        text_left_side_offset_view
                        + first_indent_view
                        + player)
                    - 2
                )
            )
        print()

    def _sort_by_score(self, tournament):
        players_list = []
        for player_id in tournament.players:
            player = Players.get_player_by_id(player_id)
            score = tournament.get_player_score(player)
            players_list.append((player, score))
        players_list.sort(key=lambda x: (x[1], x[0]), reverse=True)
        return players_list

    def max_lenght(self, tournament):
        max_lenght = []
        if len(tournament.description) \
                > DESCRIPTION_DISPLAY_MAX_SIZE:
            max_lenght.append(DESCRIPTION_DISPLAY_MAX_SIZE)
        max_lenght.append(
            len(tournament.name)
            + len("Nom : ")
            + TEXT_LEFT_SIDE_OFFSET
            )
        max_lenght.append(
            len(tournament.location)
            + len("Lieu : ")
            + TEXT_LEFT_SIDE_OFFSET
            )
        for player_id in tournament.players:
            player = Players.get_player_by_id(player_id)
            max_lenght.append(
                len(player)
                + TEXT_LEFT_SIDE_OFFSET
                + len(" (dd/mm/yyyy)   XX.X")
                )
        max_lenght.append(
            len("Contrôle du temps : ")
            + len(tournament.time_control)
            + TEXT_LEFT_SIDE_OFFSET
            )
        max_lenght.sort()
        return max_lenght[-1]


class TournamentsReportsListView:
    '''View used to show different kind of reports
    related to a tournament previously choosen.'''

    def __init__(self, list_filter):
        self.list_filter = list_filter

    def show_report(self, tournament_report, list_filter):
        if list_filter == "Name":
            self._show_players(
                tournament_report,
                "Liste des joueurs du tournoi par nom")
        if list_filter == "Ranking":
            self._show_players(
                tournament_report,
                "Liste des joueurs du tournoi par classement")
        elif list_filter == "Turn":
            if tournament_report == []:
                self._no_turn_yet()
            else:
                self._show_turns(tournament_report)
        elif list_filter == "Match":
            if tournament_report == []:
                self._no_turn_yet()
            else:
                self._show_match(tournament_report)

    def _show_players(self, tournament_report, label):
        max_lenght = 0
        for player in tournament_report:
            max_lenght = max(self._max_lenght_player(player), max_lenght)
        menu_frame, menu_label = view_utils.menu_frame_design(
            label,
            max_lenght)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        number = 0
        for player in tournament_report:
            number += 1
            self._show_player(player, number, max_lenght)
        print(menu_frame, end="\n\n")

    def _show_player(self, player, number, max_lenght):
        print(
            "\n"
            + f"Joueur n°{number}".center(max_lenght))
        print(
            text_left_side_offset_view
            + f"Nom  : {player.name}")
        print(
            text_left_side_offset_view
            + f"Prénom : {player.firstname}")
        print(
            text_left_side_offset_view
            + "Date de naissance : "
            + datetime_to_str(player.birthday))
        print(
            text_left_side_offset_view
            + f"Sexe: {player.sex}")
        print(
            text_left_side_offset_view
            + f"Rank: {str(player.rank)}\n")

    def _show_turns(self, tournament_report):
        result = {}
        max_lenght_name, max_lenght_firstname = self._max_lenght_turn(
            tournament_report)
        max_lenght_name = max(len("Nom"), max_lenght_name) + 4
        max_lenght_firstname = max(len("Prénom"), max_lenght_firstname) + 4
        lenght_birthday = len("Date de naissance")
        lenght_score = len("Score") + 2
        max_lenght = (
            len(text_left_side_offset_view)
            + len("Round") + 6
            + max_lenght_name
            + max_lenght_firstname
            + lenght_birthday
            + lenght_score
        )
        label = "Liste des tours de ce tournoi"
        menu_frame, menu_label = view_utils.menu_frame_design(
            label,
            max_lenght)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        print(
            text_left_side_offset_view
            + "Round"
            + " " * 6
            + "Nom".ljust(max_lenght_name)
            + "Prénom".ljust(max_lenght_firstname)
            + "Date de naissance"
            + "  Score")
        for turn in tournament_report:
            turn_number = turn.current_round
            for match in turn.matchs:
                player_1 = match[0][0]
                player_2 = match[1][0]
                score_1 = match[0][1]
                result = self._update_score(player_1, score_1, result)
                self._show_player_in_turn(
                    turn_number,
                    player_1,
                    result,
                    max_lenght_name,
                    max_lenght_firstname,
                    lenght_birthday)
                if not player_2 == "":
                    score_2 = match[1][1]
                    result = self._update_score(player_2, score_2, result)
                    self._show_player_in_turn(
                        turn_number,
                        player_2,
                        result,
                        max_lenght_name,
                        max_lenght_firstname,
                        lenght_birthday)
            print()
        print(menu_frame)
        print(menu_frame)
        self._show_result(
            result,
            max_lenght_name,
            max_lenght_firstname,
            lenght_birthday)
        print(menu_frame, end="\n\n")

    def _show_player_in_turn(
            self,
            turn_number,
            player,
            result,
            max_lenght_name,
            max_lenght_firstname,
            lenght_birthday):
        print(
            text_left_side_offset_view
            + turn_number
            + " " * 4
            + f"{player.name}".ljust(max_lenght_name)
            + f"{player.firstname}".ljust(max_lenght_firstname)
            + datetime_to_str(player.birthday).ljust(lenght_birthday)
            + view_utils.score_padding(result[
                Players.get_player_id(player)])
        )

    def _show_result(
            self,
            result,
            max_lenght_name,
            max_lenght_firstname,
            lenght_birthday):
        players_list = []
        for player_id, score in result.items():
            players_list.append((Players.get_player_by_id(player_id), score))
        players_list.sort(key=lambda x: (x[1], x[0]), reverse=True)
        for player, score in players_list:
            print(
                text_left_side_offset_view
                + " " * len("Round X    ")
                + f"{player.name}".ljust(max_lenght_name)
                + f"{player.firstname}".ljust(max_lenght_firstname)
                + datetime_to_str(player.birthday).ljust(lenght_birthday)
                + view_utils.score_padding(result[
                    Players.get_player_id(player)])
            )

    def _no_turn_yet(self):
        label = "Ce tournoi n'a pas encore démarré."
        menu_frame, menu_label = view_utils.menu_frame_design(
            label,
            0)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame, end="\n\n")

    def _show_match(self, tournament_report):
        width = self._max_lenght_match(tournament_report)
        label = "Liste des matchs et score de ce tournoi"
        menu_frame, menu_label = view_utils.menu_frame_design(
            label,
            width)
        width = max(width, len(menu_frame))
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame, end="")
        for turn in tournament_report:
            turn_number = turn.current_round
            print()
            for match in turn.matchs:
                self._show_peer(match, turn_number, width - 3)
        print("\n", menu_frame, end="\n\n")

    def _show_peer(self, match, turn_number, width):
        player_1 = match[0][0]
        player_2 = match[1][0]
        player_1 = (
            f"{player_1.name} {player_1.firstname} ("
            + datetime_to_str(player_1.birthday)
            + ")")
        len_player_1 = len(
            text_left_side_offset_view
            + player_1
        )
        score_1 = view_utils.score_padding(match[0][1])

        print(
            text_left_side_offset_view
            + turn_number + "\n"
            + text_left_side_offset_view
            + first_indent_view
            + player_1
            + score_1.rjust(width - len_player_1))
        if not player_2 == "":
            player_2 = (
                f"{player_2.name} {player_2.firstname} ("
                + datetime_to_str(player_2.birthday)
                + ")")
            len_player_2 = len(
                text_left_side_offset_view
                + player_2
            )
            score_2 = view_utils.score_padding(match[1][1])
            print(
                text_left_side_offset_view
                + first_indent_view
                + player_2
                + score_2.rjust(width - len_player_2))
        else:
            print("ne joue pas ce tour-ci.".center(width))

    def _max_lenght_player(self, player):
        offset = len(text_left_side_offset_view)
        max_lenght = max(
            len(f"Nom  : {player.name}"),
            len(f"Prénom : {player.firstname}"),
            len("Date de naissance : dd/mm/yyyy"),
            len(f"Sexe: {player.sex}"),
            len(f"Rank: {str(player.rank)}")
            )
        return max_lenght + offset

    def _max_lenght_turn(self, tournament_report):
        max_lenght_name = max_lenght_firstname = 0
        for match in tournament_report[0].matchs:
            player_1 = match[0][0]
            player_2 = match[1][0]
            lenght_name = len(f"{player_1.name}")
            lenght_firstname = len(f"{player_1.firstname}")
            max_lenght_name = max(lenght_name, max_lenght_name)
            max_lenght_firstname = max(
                lenght_firstname,
                max_lenght_firstname)
            if not player_2 == "":
                lenght_name = len(f"{player_2.name}")
                lenght_firstname = len(f"{player_2.firstname}")
                max_lenght_name = max(lenght_name, max_lenght_name)
                max_lenght_firstname = max(
                    lenght_firstname,
                    max_lenght_firstname)
        return max_lenght_name, max_lenght_firstname

    def _max_lenght_match(self, turns):
        width = 0
        for turn in turns:
            for match in turn.matchs:
                player_1 = match[0][0]
                player_2 = match[1][0]
                player_1 = (
                    f"{player_1.name} {player_1.firstname} "
                    + "(dd/mm/yyyy)")
                len_player_1 = len(
                    text_left_side_offset_view
                    + first_indent_view
                    + player_1
                )
                len_player_2 = 0
                if not player_2 == "":
                    player_2 = (
                        f"{player_2.name} {player_2.firstname} "
                        + "(dd/mm/yyyy)")
                    len_player_2 = len(
                        text_left_side_offset_view
                        + first_indent_view
                        + player_2
                    )
                width = max(len_player_1, len_player_2, width)
        return len(text_left_side_offset_view) + width + len("  XX.X")

    def _update_score(self, player, score, result):
        player_id = Players.get_player_id(player)
        if player_id in result:
            result[player_id] += score
        else:
            result[player_id] = score
        return result
