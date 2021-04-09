import datetime

from . import view_utils
from .views_parameters import (
                            text_left_side_offset_view,
                            first_indent_view,
                            input_label
                            )
from ..tools.tools_utils import (
                            is_date_format,
                            datetime_to_str,
                            valid_name
                            )


class AddPlayerView:

    def get_player_name(self):
        while True:
            print(
                "\n" + text_left_side_offset_view
                + "- le nom du joueur")
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

    def ask_if_player_in_list(self, players):
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

        while True:
            print(
                text_left_side_offset_view
                + "Veuillez indiquer si le joueur est déjà renseigné (o/n):")
            choice = input("   " + input_label)
            if choice == "":
                pass
            elif choice in "oO":
                return True
            elif choice in "nN":
                return False

            print("\n /** Veuillez entrer o pour oui, **\\", end="")
            print("\n /**                 n pour non. **\\")
