'''Create menu and give mean to interact with its attributes.

Classes:
    Menu
    MenuEntry

'''


class Menu:
    '''Aim to create a menu and to interact with it.'''

    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def add(self, key, option, handler):
        '''Add to the menu a key and a MenuEntry composed by the
        option to display and the handler link to this option.'''

        if key == "auto":
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, handler)

    def items(self):
        '''Return the list with all keys with their related MenuEntry.'''

        return self._entries.items()

    def max_lenght(self):
        '''return the max size of the key and option which
        will be display in order to compute the frame design.'''

        key_max_lenght = 0
        option_max_lenght = 0
        for key, option in self.items():
            if len(str(key)) > key_max_lenght:
                key_max_lenght = len(str(key))
            if len(str(option)) > option_max_lenght:
                option_max_lenght = len(str(option))
        return key_max_lenght, option_max_lenght

    def __contains__(self, key):
        '''If the key has been added in this menu return True,
        otherwise return False.'''

        return key in self._entries

    def __getitem__(self, key):
        '''return the MenuEntry link to the key.'''

        return self._entries[key]


class MenuEntry:
    '''Objet link to a menu key and composed by
    the option to display and the linked handler.'''

    def __init__(self, option, handler):
        self.option = option
        self.handler = handler

    def __repr__(self):
        return str(self.option)
