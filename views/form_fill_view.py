import re

class NewTournamentFormView:
    def get_user_setup(self):
        # Ask for the tournament name
        print("Veuillez indiquer :")
        while True:
            name = input("    - le nom du tournoi\n      >> ")
            if not(name == ""):
                break

        while True:
            location = input("    - le lieu\n      >> ")
            if not(location == ""):
                break

        while True:
            date = input("    - la date (au format jj/mm/aaaa)\n      >> ")
            if self._is_date_format(date):
                break
            else:
                print("/** Format de date invalide.  **/\")
                print("Veuillez indiquer :")

        numbers_of_turns = \
            input("    - le nombre de tours (4 par défaut)\n      >> ")
        if numbers_of_turns == None:
            numbers_of_turns = 4

        numbers_of_players = 0
        print("    - la liste des joueurs")
        print(
            "      (appuyer sur la touche \"Entrée\" sans renseigner"
            "\n       de nom pour terminer cette étape.)")
        while True:
            numbers_of_players += 1
            print(f"    - le nom du joueur {numbers_of_players})
            player_name = input("      >> ")
            if player_name == "":
                break
            print(f"    - le prénom du joueur {numbers_of_players})
            player_first_name = input("      >> ")

        time_control = input("    - le nom du tournoi\n      >> ")

        description = input("    - la description du tournoi\n      >> ")

        return (
            name,
            location,
            date,
            numbers_of_turns,
            players,
            time_control,
            description
            )

    def _is_date_format(self, string_to_test):
        date_format = re.compile("^(?:\d{2}\/){2}\d{4}$")
        if date_format.match(string_to_test):
            return True
        else:
            return False