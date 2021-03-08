import datetime

from . import view_utils
from ..models import Tournament
from ..models.menus import Menu
from ..views import views_parameters
from ..tools.tools_utils import is_date_format


class NewTournamentFormView:

    def get_user_setup(self):
        tournament = Tournament.Tournament()

        # Ask for the tournament setup
        print("\n Veuillez indiquer :")
        # Ask for the tournament name
        while True:
            tournament.name = input("    - le nom du tournoi\n      >> ")
            if not(tournament.name == ""):
                break

        # Ask for the tournament location
        while True:
            tournament.location = input("\n    - le lieu\n      >> ")
            if not(tournament.location == ""):
                break

        # Ask for the tournament date
        while True:
            date = input(
                "\n    - la date (au format jj/mm/aaaa)\n      >> ")
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
                tournament.date = date
                break
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

        # Ask for the numbers of turns
        while True:
            print("\n    - le nombre de tours ("
                f"{tournament.numbers_of_turns} par défaut)\n"
                "      (appuyer sur la touche \"Entrée\" sans renseigner"
                "\n       de valeur pour choisir la valeur par défaut.)")
            user_input = input("      >> ")
            if user_input == "":
                break
            try:
                user_input = int(user_input)
                tournament.numbers_of_turns = user_input
                break
            except:
                view_utils.alert_message_centered(
                    "Format invalide.",
                    " Veuillez choisir un",
                    " nombre entier.")
                print("\n Veuillez indiquer :", end="")

        # Ask for names of participants
        numbers_of_players = 0
        print("\n    - la liste des joueurs")
        print(
            "      (appuyer sur la touche \"Entrée\" sans renseigner"
            "\n       de nom et de prénom pour terminer cette étape.)",
            end="")
        while True:
            numbers_of_players += 1
            print(
                f"\n       - le nom et prénom du joueur {numbers_of_players}")
            player_name = input("         >> ")
            if player_name == "":
                break
            tournament.players.append(player_name)

        # Ask for time control type
        while True:
            print("\n    - le type de contrôle de temps")
            for key, value in tournament.time_control_type.items():
                print(f"         {key} : {value}")
            time_control = input("      >> ")
            if time_control in tournament.time_control_type:
                tournament.time_control = \
                    tournament.time_control_type[time_control]
                break
            else:
                print("\n /** Veuillez entrer 1, 2 ou 3. **\\")
            print("\n Veuillez indiquer :", end="")

        tournament.description = input(
            "\n    - la description du tournoi\n      >> ")

        return tournament

    def get_user_validation(self):
        while True:
            print("\n Est-ce que les informations sur ce tournoi sont correctes ? (o/n)")
            user_input = input("      >> ")
            if user_input in "oO":
                return True
            elif user_input in "nN":
                return False
            else:
                print("\n /** Veuillez entrer o pour oui, **\\", end="")
                print("\n /**                 n pour non. **\\")

    def new_tournament_summary(self, tournament):
        max_lenght = tournament.max_lenght()
        menu_frame, menu_label = view_utils.menu_frame_design(
            "Résumé du tournoi",
            max_lenght)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        print(f"    Nom  : {tournament.name}")
        print(f"    Lieu : {tournament.location}")
        print(f"    Date : {tournament.date:%d}/"
            + f"{tournament.date:%m}/"
            + f"{tournament.date:%Y}")
        print(f"    Nombre de tours : {tournament.numbers_of_turns}")
        print(f"    Liste des joueurs :")
        for player in tournament.players:
            print(" " * views_parameters.MENU_LEFT_SIDE_OFFSET
                + player.center(max_lenght
                + views_parameters.TEXT_LEFT_SIDE_OFFSET))
        print(f"    Contrôle du temps : {tournament.time_control}")
        print(f"    Description :")
        if not tournament.description == "":
            description = tournament.description.split()
            description_display_size = (max_lenght
                + views_parameters.TEXT_LEFT_SIDE_OFFSET
                -views_parameters.MENU_LEFT_SIDE_OFFSET)
            size = (
                views_parameters.TEXT_LEFT_SIDE_OFFSET
                + views_parameters.FIRST_INDENT)
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
        print(menu_frame)


class StarttournamentView:
    pass

