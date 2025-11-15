from datetime import datetime


def date_refactor(date_string):
    datetime_object = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
    return datetime_object
