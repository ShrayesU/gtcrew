from django.utils.timezone import now


def get_current_year():
    return now().year
