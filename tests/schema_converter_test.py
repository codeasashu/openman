import unittest
from openman import SchemaConvertor

class TestSchemaConverter(unittest.TestCase):

    def test_convert(self):
        # int
        schema = SchemaConvertor.convert(1)
        self.assertEqual(
            dict(format = 'int32',type = 'integer'),
            schema
        )

        # str
        schema = SchemaConvertor.convert("1")
        self.assertEqual(dict(type = 'string'), schema)

        # lists
        schema = SchemaConvertor.convert([1,2,3])
        self.assertEqual(dict(
                type = 'array',
                items = dict(
                    type = 'integer',
                    format='int32'
                )
            ),
            schema)
        
        schema = SchemaConvertor.convert([1,2,'a'])
        self.assertEqual(dict(
                type = 'array',
                items = dict(
                    allOf = [
                        dict(
                            type = 'integer',
                            format='int32'
                        ),
                        dict(
                            type = 'string',
                        ),
                    ]
                )
            ),
            schema)

        schema = SchemaConvertor.convert([dict(a='b'), dict(c=3)])
        self.assertEqual(
            dict(
                type = 'array',
                items = dict(
                    allOf = [
                        dict(
                            type = 'object',
                            properties = dict(
                                a =  dict(type = 'string')
                            ),
                            required = ['a']
                        ),
                        dict(
                            type = 'object',
                            properties = dict(
                                c =  dict(type = 'integer', format='int32')
                            ),
                            required = ['c']
                        )
                    ]
                )
            ),
            schema)

        # objects
        schema = SchemaConvertor.convert(dict(a='b', c=dict(d='e')))
        self.assertEqual(
            dict(
                type = 'object',
                properties = dict(
                    a = dict(type='string'),
                    c = dict(
                        type = 'object',
                        properties = dict(
                            d = dict(type='string'),
                        ),
                        required = ['d'],
                    ),
                ),
                required = ['a', 'c']
            ), schema)