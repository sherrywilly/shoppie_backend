from datetime import datetime


def genKey(phone):
    return str(phone) + str(datetime.date(datetime.now())) + "deepsense"