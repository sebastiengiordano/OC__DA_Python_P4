from ..views.form_fill_view import NewTournamentFormView


class NewTournamentFormController:

    def __init__(self):
        self._view = NewTournamentFormView()

    def __call__(self):
        # 1. Ask tournament
        (name,
        location,
        date,
        numbers_of_turns,
        players,
        time_control,
        description
        ) = self._view.get_user_setup()

        # 2. Ask user choice
        user_choice = self._view.get_user_choice()
