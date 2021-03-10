from re import compile
import datetime


def is_date_format(string_to_test):
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
