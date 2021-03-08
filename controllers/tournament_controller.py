from . import main_controllers
from ..views.tournament_view import NewTournamentFormView
from ..views.menu_views import NewTournamentStartView
from ..models.menus import Menu 


class NewTournamentFormController:

    def __init__(self):
        self._view = NewTournamentFormView()

    def __call__(self):
        # 1. Ask for tournament setup
        tournament = self._view.get_user_setup()

        # 2. Show tournament summary
        self._view.new_tournament_summary(tournament)

        # 3. Ask user validation
        # (verfication that the tournament has no mistake)
        user_validation = self._view.get_user_validation()
        if not user_validation:
            return main_controllers.HomeMenuController()

        # 4. Save the tournament setup

        # 5. Ask user choice (start tournament / back to main menu)
        return NewTournamentStartController(tournament)


class NewTournamentStartController:
    
    def __init__(self, tournament):
        self.tournament = tournament
        self.menu = Menu()
        self._view = NewTournamentStartView(self.menu)
    
    def __call__(self):
        # 1. Generate the new tournament start menu
        self.menu.add(
            "auto",
            "Lancer le tournoi",
            main_controllers.StartTournamentController(tournament))
        self.menu.add(
            "auto",
            "Revenir au menu principal",
            main_controllers.HomeMenuController())
        self.menu.add(
            "q",
            "Quitter l'application",
            main_controllers.ExitApplicationController())

        # 2. Ask user choice
        user_choice = self._view.get_user_choice()

        # 3. Return the controller link to user choice
        #    to the main controller
        return user_choice.handler
