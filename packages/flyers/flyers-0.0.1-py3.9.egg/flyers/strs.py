def is_emtpy(s: str):
    return s is None or len(s) == 0


def is_blank(s: str):
    return is_emtpy(s.lstrip().rstrip())


def repeat(s: str, n: int):
    return s * n
