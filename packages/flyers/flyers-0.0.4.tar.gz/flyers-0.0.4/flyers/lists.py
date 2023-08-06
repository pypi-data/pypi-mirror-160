import random


def get_random(l: list):
    if len(l) == 0:
        return None
    return l[random.randint(0, len(l) - 1)]
