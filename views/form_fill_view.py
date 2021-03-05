from ..models.Tournament import Tournament
from .menu_views import NewTournamentStartView
from . import utils


class NewTournamentFormView:
    def get_user_setup(self):
        tournament = Tournament()

        # Ask for the tournament setup
        print(" Veuillez indiquer :")
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
            tournament.date = input(
                "\n    - la date (au format jj/mm/aaaa)\n      >> ")
            if tournament._is_date_format(tournament.date):
                break
            else:
                print(" /** Format de date invalide.  **\\")
                print(" Veuillez indiquer :", end="")

        # Ask for the numbers of turns
        print("\n    - le nombre de tours ("
            f"{tournament.numbers_of_turns} par défaut)\n"
            "      (appuyer sur la touche \"Entrée\" sans renseigner"
            "\n       de valeur pour choisir la valeur par défaut.)")
        user_input = input("      >> ")
        if not user_input == "":
            tournament.numbers_of_turns = user_input

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
                print("\n /** Veuillez entrer 1, 2 ou 3.  **\\")
            print(" Veuillez indiquer :", end="")

        tournament.description = input(
            "\n    - la description du tournoi\n      >> ")

        self._new_tournament_summary(tournament)

        return tournament

    def get_user_choice(self):
        menu = NewTournamentStartView()
        menu.add()
        menu_frame, menu_label = utils.menu_frame_design(
            "Résumé du tournoi",
            max_lenght)

    def get_user_validation(self):
        while True:
            print("\n Est-ce que les informations sur ce tournoi sont correctes ? (o/n)")
            user_input = input("      >> ")
            if user_input in "oO":
                return True
            elif user_input in "nN":
                return False
            else:
                print("\n /** Veuillez entrer o pour oui,  **\\")
                print("\n /**                 n pour non.  **\\")

    def _new_tournament_summary(self, tournament):
        max_lenght = tournament.max_lenght() + 4
        menu_frame, menu_label = utils.menu_frame_design(
            "Résumé du tournoi",
            max_lenght)
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        print(f"    Nom  : {tournament.name}")
        print(f"    Lieu : {tournament.location}")
        print(f"    Date : {tournament.date}")
        print(f"    Nombre de tours : {tournament.numbers_of_turns}")
        print(f"    Liste des joueurs :")
        for player in tournament.players:
            print(player.center(max_lenght))
        print(f"    Contrôle du temps : {tournament.time_control}")
        print(f"    Description :")
        if not tournament.description == "":
            description = tournament.description.split()
            description_display_size = max_lenght - 2
            size = 0
            print("    ", end="")
            for texte in description:
                if size + len(texte) < description_display_size:
                    print(texte + " ", end="")
                    size += len(texte + " ")
                else:
                    print("\n    " + texte + " ", end="")
                    size = 0
            print("")
        print(menu_frame)
