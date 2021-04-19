def menu_frame_design(menu_name, width_menu):
    '''This function return the frame of a menu.
    '''

    # Add blank around menu name
    menu_name = "*  " + menu_name + "  *"

    # Calculate width of the menu
    menu_name_size = len(menu_name)
    if menu_name_size > width_menu:
        width_menu = menu_name_size

    # Generate the menu frame design
    menu_frame = " /"
    menu_frame += "*" * width_menu
    menu_frame += "/"

    if (width_menu - menu_name_size) % 2:
        menu_name += "*"
    menu_label_fill_number = ((width_menu - menu_name_size) // 2)
    menu_label = " /"
    menu_label += "*" * menu_label_fill_number
    menu_label += menu_name
    menu_label += "*" * menu_label_fill_number
    menu_label += "/"

    return menu_frame, menu_label


def alert_message_centered(*args):
    max_size = 0
    print("")
    for elem in args:
        if max_size < len(elem):
            max_size = len(elem)
    if max_size % 2:
        max_size += 1

    print(" /" + "*" * (max_size + 6) + "\\")

    for elem in args:
        print(" /** ", end="")
        print(elem.center(max_size), end="")
        print(" **\\")

    print(" /" + "*" * (max_size + 6) + "\\")


def score_padding(score):
    if score - int(score) <= 0.001:
        score = int(score)
        return f"{score}".ljust(3).rjust(6)
    elif score - int(score) > 0:
        return f"{score}".rjust(6)
