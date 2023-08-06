import base64
import uuid


def uuid4() -> str:
    return str(uuid.uuid4())


def uuid4_no_symbol() -> str:
    return str(uuid.uuid4()).replace('-', '')


# base64 utils

def base64_encode(s):
    return base64.b64encode(s.encode()).decode('utf-8')


def base64_decode(s):
    return base64.b64decode(s).decode('utf-8')
