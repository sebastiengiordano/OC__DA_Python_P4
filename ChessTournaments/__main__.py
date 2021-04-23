'''Entry point of the application.

Functions:
    main

'''

from .controllers.main_controllers import ApplicationController


def main():
    ''' main function which performed the following actions:
            - Instantiate ApplicationController()
            - Start the application
    '''
    app = ApplicationController()
    app.start()


################
# Run the code #
################
if __name__ == "__main__":
    main()
