class MenuEntry:

    def __init__(self, option, handler):
        self.option = option
        self.handler = handler

    def __repr__(self):
        return str(self.option)


class Menu:
    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def add(self, key, option, handler):
        if key == "auto":
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, handler)

    def items(self):
        return self._entries.items()

    def max_lenght(self):
        key_max_lenght = 0
        option_max_lenght = 0
        for key, option in self.items():
            if len(str(key)) > key_max_lenght:
                key_max_lenght = len(str(key))
            if len(str(option)) > option_max_lenght:
                option_max_lenght = len(str(option))
        return key_max_lenght, option_max_lenght

    def __contains__(self, key):
        return key in self._entries

    def __getitem__(self, key):
        return self._entries[key]


if __name__ == "__main__":
    menu = Menu()
    menu.add("auto", "première option du menu", lambda: None)
    menu.add("auto", "deuxième option du menu", lambda: None)
    menu.add("q", "quitter le menu", lambda: None)
    print(menu._entries)
