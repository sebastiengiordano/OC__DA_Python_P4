from ..views.form_fill_view import NewTournamentFormView
from .main_controllers import HomeMenuController
# from ..models.Tournaments import Tournaments


class NewTournamentFormController:

    def __init__(self):
        self._view = NewTournamentFormView()

    def __call__(self):
        # 1. Ask for tournament setup
        tournament = self._view.get_user_setup()

        # 2. Ask user validation
        # (verfication that the tournament has no mistake)
        user_validation = self._view.get_user_validation()
        if not user_validation:
            return main_controllers.HomeMenuController()

        # 3. Save the tournament setup

        # 4. Ask user choice (start tournament / back to main menu)
        user_choice = self._view.get_user_choice()
