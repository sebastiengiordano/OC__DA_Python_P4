from . import view_utils


class MenuView:

    def __init__(self, menu):
        self.menu = menu
        self._menu_name = ""

    def _display_menu(self):
        key_max_lenght, option_max_lenght = self.menu.max_lenght()
        menu_frame, menu_label = view_utils.menu_frame_design(
            self._menu_name,
            key_max_lenght
            + option_max_lenght
            + len("  : "))
        print("\n" + menu_frame)
        print(menu_label)
        print(menu_frame)
        for key, entry in self.menu.items():
            space_before_key = " " * (key_max_lenght - len(key))
            print(f"   {space_before_key}{key}: {entry.option}")
        print(menu_frame)

    def _get_user_key(self):
        return input("   >> ")

    def get_user_choice(self):
        while True:
            # Display the menu to user
            self._display_menu()
            # Ask the user its choice
            choice = self._get_user_key()
            # Validate the user choice
            if choice in self.menu:
                # Return the user choice
                return self.menu[choice]


class HomeMenuView(MenuView):

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Menu d'acceuil"


class NewTournamentView(MenuView):

    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Création d'un nouveau tournoi"


class NewTournamentStartView(MenuView):
    
    def __init__(self, menu):
        super().__init__(menu)
        self._menu_name = "Démarrer ce nouveau tournoi"
