import datetime

from . import view_utils
from .views_parameters import (
                            text_left_side_offset_view,
                            first_indent_view,
                            input_label
                            )
from ..tools.tools_utils import (
                            is_date_format,
                            valid_name
                            )


class AddPlayerView:

    def get_player_name(self):
        while True:
            print(
                "\n" + text_left_side_offset_view
                + "- le nom du joueur")
            player_name = input("   " + input_label)
            for elem in player_name:
                if elem.isalpha() or elem.isspace() or elem == "\'":
                    view_utils.alert_message_centered(
                        "Format invalide.",
                        "Le nom ne doit être",
                        "composé que de lettre.")
                    print("\n /** Format invalide. **\\")
                    print("\n Veuillez indiquer :", end="")
                    break
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
            if sex in "mfMF":
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
                + " de valeur pour choisir la valeur 0.\n)"
                + input_label)
            if rank.isdigit():
                return int(rank)
            elif rank == "":
                return 0
            else:
                print("\n /** Réponse invalide. **\\")
            print("\n Veuillez indiquer :", end="")
