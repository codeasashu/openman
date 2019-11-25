from .utils import python2schematypes
import json
import jsonpath_rw

class  SchemaConvertor(object):

    def filter_unique_schema(self, schemas):
        uniq = []
        prevschema = None
        while len(schemas):
            newschema = schemas.pop(0)
            if prevschema == newschema:
                continue
            prevschema = newschema
            uniq.append(newschema)
        return  uniq
    
    @property
    def IGNOREPROP(self):
        return f'__{self.__class__.__name__}__'
    
    @property
    def IGNOREPROPKEYVAL(self):
        return f'__{self.IGNOREPROP}__all__'

    def _walker(self, item, ignore=False):
        if item is None:
            return {}
        (_type, _format) = python2schematypes[type(item)]
        schema = dict(type = _type)
        if isinstance(item, str):
            if item == self.IGNOREPROP:
                schema = dict(additionalProperties = {})
        elif isinstance(item, int):
            schema['format'] = _format
        elif isinstance(item, dict):
            schema['properties'] = dict()
            if(len(item.keys()) > 0):
                schema['required'] = []
            for k, v in item.items():
                if v == self.IGNOREPROPKEYVAL:
                    schema['properties']['additionalProperties'] = {}
                else:
                    schema['required'].append(k)
                    schema['properties'][k] = self._walker(v)
        elif isinstance(item, list):
            uniqueschemas = self.filter_unique_schema(
                [self._walker(v) for v in item])
            schema['items'] = dict()
            if len(uniqueschemas) > 1:
                schema['items']['allOf'] = uniqueschemas
            elif uniqueschemas:
                schema['items'] = uniqueschemas[0]
        return schema
    
    def parse_ignore(self, expr):
        type_explode = expr.split(':')
        if len(type_explode) > 1 and type_explode[-1] == 'a':
            return ''.join(type_explode[:-1]), True
        return expr, False
    
    def filter_item(self, item, ignores=[]):
        for ignore in ignores:
            ignore_expr, ignore_all = self.parse_ignore(ignore)
            jsonpath_expr = jsonpath_rw.parse(ignore_expr)
            matches = jsonpath_expr.find(item)
            ignoreprop = self.IGNOREPROPKEYVAL if ignore_all else self.IGNOREPROP
            for match in matches:
                item = self.json_update_path(item, self.json_get_path(match), ignoreprop)
        return item
    
    def json_get_path(self, match):
        '''return an iterator based upon MATCH.PATH. Each item is a path component,
        start from outer most item.'''
        if match.context is not None:
            for path_element in self.json_get_path(match.context):
                yield path_element
            yield str(match.path)
    
    def json_update_path(self, json, path, value):
        '''Update JSON dictionnary PATH with VALUE. Return updated JSON'''
        try:
            first = next(path)
            # check if item is an array
            if first.startswith('[') and first.endswith(']'):
                try:
                    first = int(first[1:-1])
                except ValueError:
                    pass
            json[first] = self.json_update_path(json[first], path, value)
            return json
        except StopIteration:
            return value

    @classmethod
    def convert(cls, item, format_to=None, ignore=[]):
        # Mark the item for filtering
        item = cls().filter_item(item, ignore)
        schema = cls()._walker(item)
        if format_to and format_to in ['json']:
            return json.dumps(schema)
        return schema