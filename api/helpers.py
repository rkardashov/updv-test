import re
from django.db import models


class IDTypes(models.TextChoices):
    EMAIL = ("email", "Email")
    PHONE = ("phone", "Phone number")
    UNKNOWN = ("unknown", "Unknown")


def get_idtype(username):
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', username):
        return IDTypes.EMAIL

    if re.match(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', username):
        return IDTypes.PHONE

    return IDTypes.UNKNOWN
