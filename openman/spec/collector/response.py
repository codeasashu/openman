from openman.utils import camelize


class ResponseCollector:
    def __init__(self):
        self.responses = {}
        self.examples = {}
        self.contents = {}

    @staticmethod
    def get_unique_key(code, content_type):
        return f"{code}/{content_type}"

    def add_example(self, code, content_type, title, example, **kwargs):
        title = camelize(title)
        example = {
            "value": example,
            "x-response-id": kwargs.pop("response_id", ""),
        }
        if code in self.examples.keys():
            if content_type in self.examples[code].keys():
                self.examples[code][content_type][title] = example
            else:
                self.examples[code][content_type] = dict()
                self.examples[code][content_type][title] = example
        else:
            self.examples[code] = dict()
            self.examples[code][content_type] = dict()
            self.examples[code][content_type][title] = example

    def add_content(self, code, content_type, title, schema):
        schema["title"] = title
        key = self.get_unique_key(code, content_type)
        if key not in self.contents.keys():
            self.contents[key] = schema
        else:
            if "oneOf" in self.contents[key].keys():
                self.contents[key]["oneOf"] += [schema]
            else:
                self.contents[key] = {"oneOf": [self.contents[key], schema]}

    def get_schema(self, code, content_type):
        key = self.get_unique_key(code, content_type)
        return self.contents[key]

    def get_example(self, code, content_type):
        return self.examples[code][content_type]

    def get_content(self, code, content_type):
        schema = self.get_schema(code, content_type)
        examples = self.get_example(code, content_type)
        content = dict()
        content[content_type] = dict(schema=schema, examples=examples)
        return content

    def add_response(self, code, content_type, title):
        self.responses[code] = dict(
            content=self.get_content(code, content_type), description=title
        )

    def collect(self):
        return self.responses

    def add(self, code, content_type, schema, title, example, **kwargs):
        self.add_example(code, content_type, title, example, **kwargs)
        self.add_content(code, content_type, title, schema)
        self.add_response(code, content_type, title)
        # response_examples[camelize(response.description)] = {"value": response.body, 'x-response-id': response.id}
        """
            if response_contents.get(key, None) is None:
                response_contents[key] = schema
            else:
                toins = None
                if "oneOf" in response_contents[key].keys():
                    toins = response_contents[key]['oneOf']
                    toins.append(schema)
                else:
                    toins = [response_contents[key], schema]
                response_contents[key] = {"oneOf": toins}
            response_content = dict()
            response_content[response.content_type] = dict(
                schema = response_contents[key],
                examples = response_examples
                # examples = {
                    # camelize(response.description): {
                        # 'value': response.body,
                        # 'x-response-id': response.id
                    # },
                # },
            )
            response_schema[int(response.code)] = dict(
                content = response_content,
                description = response.description
            )
        """
