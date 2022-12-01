import random
import string
from ..models import Tournament


def generate():
    while True:
        list_ascii_letters = [_ for _ in (string.ascii_letters + string.digits)]
        list_string = random.choices(list_ascii_letters, k=12)
        uid_string = "".join(list_string)

        if not Tournament.objects.filter(uid=uid_string):
            break

    return uid_string

