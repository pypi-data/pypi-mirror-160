class StatusCodes(object):
    SUCCESS = 0


def success(data=None):
    return {'code': StatusCodes.SUCCESS, 'message': 'success', 'data': data}


def failure(code: int, message: str = None):
    return {'code': code, 'message': message, 'data': None}
