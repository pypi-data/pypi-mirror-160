def check_null(s, name: str):
    if s is None:
        raise ValueError("The '{}' cannot be null".format(name))


def check_blank(s: str, name: str):
    if not str or len(s) == 0:
        raise ValueError("The '{}' cannot be blank".format(name))
