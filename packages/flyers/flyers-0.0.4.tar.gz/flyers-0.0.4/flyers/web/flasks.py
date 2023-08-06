from flask import jsonify, Flask
from flask_expects_json import ValidationError
from typing import Dict
from . import rest

SUPPORTS_TYPE = ['str', 'int', 'float', 'bool', 'list']


def succeed(data):
    return jsonify(rest.success(data))


def error(message):
    return jsonify(rest.failure(-1, message))


def abort(msg, code):
    return error(msg), code


def generate_schema(clazz):
    result = {
        'type': 'object',
        'properties': {},
    }

    include_list = []
    exclude_list = []
    fields = []
    for field_name in dir(clazz):
        if field_name.startswith('__'):
            continue

        if field_name == 'required_include':
            include_list = getattr(clazz, field_name)
            continue

        if field_name == 'required_exclude':
            exclude_list = getattr(clazz, field_name)
            continue

        fields.append(field_name)
        t = getattr(clazz, field_name)
        if t == str:
            ts = 'string'
        elif t == bool:
            ts = 'boolean'
        elif t == int or t == float:
            ts = 'number'
        elif t == list:
            ts = 'array'
        else:
            ts = None

        if not ts:
            raise Exception('invalid type: {}, only supports: {}'.format(t, SUPPORTS_TYPE))

        result['properties'][field_name] = {
            'type': ts
        }

    if include_list.__contains__('all'):
        required = fields
    else:
        required = include_list

    for each in exclude_list:
        if required.__contains__(each):
            required.remove(each)

    result['required'] = required
    return result


def bind_body(data: Dict, clazz):
    obj = clazz()
    ignore = ['required_include', 'required_exclude']
    for field_name in dir(clazz):
        if field_name.startswith('__') or ignore.__contains__(field_name):
            continue

        if field_name not in data:
            raise ValueError('The {} field not in data'.format(field_name))
        setattr(obj, field_name, data[field_name])
    return obj


def add_expects_json_handler(app: Flask):
    @app.errorhandler(400)
    def bad_request(e):
        if isinstance(e.description, ValidationError):
            original_error = e.description
            return abort(original_error.message, 400)
        else:
            return abort(e.description, 400)
