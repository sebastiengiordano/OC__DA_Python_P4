'''View of all the menus.

Classes:
    MenuView
    HomeMenuView
    NewTournamentMenuView
    NewTournamentStartMenuView
    TurnMenuView
    ChoiceTournamentMenuView
    TournamentTerminatedMenuView
    RankingUpdateMenuView
    ChoicePlayerMenuView
    GenerateReportsMenuView

'''

from . import view_utils
from .views_parameters import input_label


class MenuView:
    '''Mother class of all other menus.

    Aim to display the menu and get the user choice.

    '''

    def __init__(self, menu):
        self._menu = menu
        self._menu_name = ""

    def _display_menu(self):
        key_max_lenght, option_max_lenght = self._menu.max_lenght()
        menu_frame, menu_label = view_utils.menu_frame_design(
            self._menu_name,
            key_max_lenght
            + option_max_lenght
            + len("  : "))
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        for key, entry in self._menu.items():
            space_before_key = " " * (key_max_lenght - len(key))
            print(f"   {space_before_key}{key}: {entry.option}")
        print(menu_frame)

    def _get_user_key(self):
        return input(input_label)

    def get_user_choice(self):
        while True:
            # Display the menu to user
            self._display_menu()
            # Ask the user its choice
            choice = self._get_user_key()
            # Validate the user choice
            if choice in self._menu:
                # Return the user choice
                return self._menu[choice]


class HomeMenuView(MenuView):
    '''Home menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Menu d'acceuil"


class NewTournamentMenuView(MenuView):
    '''New tournament menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Création d'un nouveau tournoi"


class NewTournamentStartMenuView(MenuView):
    '''New tournament start menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Démarrer ce nouveau tournoi"


class TurnMenuView(MenuView):
    '''Turn menu view'''

    def __init__(self, menu, tour):
        super().__init__(menu)
        self._menu_name = f"Menu du tour n°{tour}"


class ChoiceTournamentMenuView(MenuView):
    '''Choice tournament menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Démarrer / Reprendre un tournoi"


class TournamentTerminatedMenuView(MenuView):
    '''Tournament terminated menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Le tournoi sélectionné est terminé."


class RankingUpdateMenuView(MenuView):
    '''Ranking update menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Mettre à jour les classements."


class ChoicePlayerMenuView(MenuView):
    '''Choice player menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Valider le choix du joueur."


class GenerateReportsMenuView(MenuView):
    '''Generate reports menu view'''

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Générer des rapports."
