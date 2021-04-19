from re import compile
import datetime


def is_date_format(string_to_test):
    '''Check if the variable is could be set as datetime type
    with the following format:
        dd/mm/yyyy
            If its the case, check if the date value are coherent.
                If its not the case a error message is sent.
                Otherwise, the datetime is return
            Otherwise return none
    '''
    date_format = compile(r"^(\d?\d)\W(\d?\d)\W(\d{4})$")
    string_match = date_format.match(string_to_test)
    if string_match:
        try:
            date = datetime.date(
                int(string_match.group(3)),
                int(string_match.group(2)),
                int(string_match.group(1)))
        except ValueError as exception:
            return str(exception)
        return date
    else:
        return None


def datetime_to_str(date):
    '''Check the date type, if its a datime type:
    Return the date with the following format:
        dd/mm/yyyy
    Otherwise return ""
    '''
    if isinstance(date, datetime.date):
        str_date = (
            f"{date.day:0>2d}/"
            + f"{date.month:0>2d}/"
            + str(date.year)
            )
        return str_date
    return ""


def valid_name(name):
    for elem in name:
        if not(
                elem.isalpha()
                or elem.isspace()
                or elem == "\'"):
            return False

    return True
