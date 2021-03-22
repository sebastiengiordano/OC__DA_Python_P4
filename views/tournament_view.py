import datetime


from .player_views import AddPlayerView
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
                + " de valeur pour choisir la date d'aujourd'hui.)"
                + input_label)
            if date == "":
                date = datetime.date.today()
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
                break
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


class StarttournamentView:
    pass


class NewTournamentAddPlayerView:

    def __init__(self):
        self._players = Players.players
        self._view = AddPlayerView()

    def __call__(self):
        # 1. Ask for player name
        name = self._view.get_player_name()

        # 2. Check if this name is already in Players.players list
        players_with_same_name = Players.is_player_exist(name)
        if players_with_same_name == []:
            # 2.1 This is a new play, add to the list
            self._view

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
                + "- la date (au format jj/mm/aaaa)\n"
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
                    + "   Anniversaire: " + datetime_to_str(player.birthday)
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
