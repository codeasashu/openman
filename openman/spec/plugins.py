from apispec import BasePlugin
from apispec.exceptions import DuplicateComponentNameError
from ..utils import camelize

class MultiOperationBuilderPlugin(BasePlugin):
    def __init__(self, refs=False):
        self.refs = refs
        self._reserved_keys = ['oneOf', 'allOf', 'anyOf']
        self.counter = {'schema': {}, 'example': {}}

    def init_spec(self, spec):
        super().init_spec(spec)
        self.spec = spec
        self.duplicate_schemas = {}
        self.duplicate_examples = {}
    
    def add_ref_schema(self, name, schema):
        #_name = self._get_uniq_refname('schema', name)
        try:
            self.spec.components.schema(name, schema)
        except DuplicateComponentNameError as e:
            name = self._get_uniq_refname('schema', name)
            self.add_ref_schema(name, schema)
        return self.spec.get_ref('schema', name)
    
    def add_ref_example(self, name, body):
        try:
            self.spec.components.example(name, body)
        except DuplicateComponentNameError as e:
            name = self._get_uniq_refname('example', name)
            self.add_ref_example(name, body)
        return self.spec.get_ref('example', name)
    
    def _get_uniq_refname(self, key, name):
        if self.counter[key].get(name, None) is None:
            self.counter[key] = {name: 0}
            _name = name
        else:
            self.counter[key][name] += 1
        _name = name + '_' + str(self.counter[key][name] + 1)
        return _name

    def _fix_response_schema(self, path, operations):
        for key, value in operations.items():
            for code, response in value.get('responses', {}).items():
                if 'content' in response:
                    for content_type, schema in response['content'].items():
                        opskey = camelize(path +' '+ key + str(code)) + content_type

                        #schemafix
                        if self.duplicate_schemas.get(opskey, None) is None:
                            if self.refs:
                                schema['schema'] = self.add_ref_schema('schema' +camelize(path +' '+ key + str(code)), schema['schema'])
                            self.duplicate_schemas[opskey] = [schema['schema']]
                        else:
                            if self.refs:
                                schema['schema'] = self.add_ref_schema('schema' +camelize(path +' '+ key + str(code)), schema['schema'])
                            self.duplicate_schemas[opskey].append(schema['schema'])
                            schema['schema'] = dict(
                                oneOf = [
                                    schema for schema in self.duplicate_schemas.get(opskey)]
                            )
                        #examplefix
                        if 'examples' in schema:
                            if self.duplicate_examples.get(opskey, None) is None:
                                if self.refs:
                                    for desc, example_item in schema['examples'].items():
                                        schema['examples'][desc] = self.add_ref_example(
                                            'example' +camelize(path +' '+ key + str(code)),
                                            example_item)
                                self.duplicate_examples[opskey] = [schema['examples']]
                            else:
                                if self.refs:
                                    for desc, example_item in schema['examples'].items():
                                        schema['examples'][desc] = self.add_ref_example(
                                            'example' +camelize(path +' '+ key + str(code)),
                                            example_item)
                                self.duplicate_examples[opskey].append(schema['examples'])
                                for example in self.duplicate_examples.get(opskey):
                                    for example_name, example_value in example.items():
                                        schema['examples'][example_name] = example_value
    
    def operation_helper(self, path, operations, **kwargs):
        """Operation helper that add `deprecated` flag if in `kwargs`
        """
        self._fix_response_schema(path, operations)