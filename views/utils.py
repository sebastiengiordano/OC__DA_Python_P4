def menu_frame_design(menu_name, key_max_lenght, option_max_lenght):
    '''This function return the frame of a menu.
    '''

    # Add blank around menu name
    menu_name = "  " + menu_name + "  "

    # Calculate width of the menu
    width_menu = (key_max_lenght + option_max_lenght + len("  : "))
    menu_name_size = len(menu_name)
    if menu_name_size > width_menu:
        width_menu = menu_name_size

    # Generate the menu frame design
    menu_frame = "/"
    menu_frame += "*" * width_menu
    menu_frame += "/"

    if (width_menu % 2) and not (menu_name_size % 2):
        menu_name += "*"
    menu_label_fill_number = ((width_menu - menu_name_size) // 2)
    menu_label = "/"
    menu_label += "*" * menu_label_fill_number
    menu_label += menu_name
    menu_label += "*" * menu_label_fill_number
    menu_label += "/"

    return menu_frame, menu_label