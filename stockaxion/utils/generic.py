from datetime import datetime


def get_date():
    return datetime.now().strftime("%Y%m%d")
