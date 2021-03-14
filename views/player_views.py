from .views_parameters import input_label


class AddPlayerView:

    def get_player_name(self):
        print(
            "\n" + text_left_side_offset_view
            + "- le nom du joueur")
        player_name = input("   " + input_label)
        return player_name

    def get_player_firstname(self):
        print(
            "\n" + text_left_side_offset_view
            + "- le prénom du joueur")
        return input("   " + input_label)

    def get_player_birthday(self):
        pass

    def get_player_sex(self):
        pass

    def get_player_rank(self):
        pass


class NewTournamentAddPlayerView:

    def get_player_name(self, numbers_of_players):
        print(
            "\n" + text_left_side_offset_view
            + f"- le nom du joueur {numbers_of_players}")
        player_name = input("   " + input_label)
        return player_name

    def get_player_firstname(self):
        print(
            "\n" + text_left_side_offset_view
            + "- le prénom du joueur")
        return input("   " + input_label)

    def get_player_birthday(self):
        while True:
            birthday = input(
                "\n" + text_left_side_offset_view
                "- la date (au format jj/mm/aaaa)\n"
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
                "- le sexe du joueur (M/F)\n"
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
                "- le classement du joueur\n"
                + text_left_side_offset_view + fisrt_indent_view
                "(appuyer sur la touche \"Entrée\" sans renseigner"
                + "\n" + text_left_side_offset_view + fisrt_indent_view
                + " de valeur pour choisir la valeur 0.)")
                + input_label)
            if isinstance(rank, int):
                return rank
            elif:
                rank = ""
                return 0
            else:
                print("\n /** Réponse invalide. **\\")
            print("\n Veuillez indiquer :", end="")
