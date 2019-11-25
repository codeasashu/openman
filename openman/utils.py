import re

_postman_env_regex = r"\{\{[a-zA-Z0-9_.]+\}\}"

DEFAULT_STATUS_CODE = 200

# https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#dataTypeFormat
python2schematypes = {
    int: ('integer', 'int32'),
    list: ('array', None),
    str: ('string', None),
    bool: ('boolean', "null"),
    dict: ('object', None),
}


def filter_env_var(item):
    return re.findall(_postman_env_regex, item)

def is_requestitem(item):
    return isinstance(item, dict) and \
        ('name' in item) and \
        ('request' in item) and \
        ('item' not in item)

def is_request(item):
    return isinstance(item, dict) and \
        ('method' in item) and \
        ('item' not in item)

def is_response(item):
    return isinstance(item, dict) and \
        ('originalRequest' in item) and \
        ('item' not in item)

def is_folder(item):
    return isinstance(item, dict) and \
        set(['name', 'item', 'description']).issubset(set(item.keys()))

def is_collection(item):
    return isinstance(item, dict) and \
        ('info' in item) and \
            ('schema' in item['info'])

def format_path(path):
    path = '/'.join(path) if isinstance(path, list) \
        else path
    return '/'+path if path[0] != '/' else path

def is_disabled(item):
    return item.get('disabled', False) is True

def map_to_dict(items):
    return {item.get('key') : item.get('value') \
        for item in items if not is_disabled(item)}

def strip_charset(item):
    item = re.sub(r'charset\=.+', '',str(item))
    return item.replace(';','').rstrip()

def camelize(string):
    return ''.join(a.capitalize() for a in re.split('([^a-zA-Z0-9])', string) if a.isalnum())

def sanitized(name):
    return name and re.sub('^[^a-zA-Z_]+', '', re.sub('[^0-9a-zA-Z_]', '', name))
