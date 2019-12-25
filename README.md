# Openman

A postman to openapi spec conversion tool, which automatically

- Converts your postman collection (2.1) to OpeanAPI Spec (3.0.0)
- Mocks your openapi collection to generate responses from postman examples

Other than these, this tool can easily handle ignored fields in responses (explained below)

**NOTE** Please use postman collection ver 2.1 export (and not 2.0 or earlier). This library only support postman collection 2.1

## Installation

**NOTE** This repo needs you to have python 3.5+ installed

As of now, I haven't pushed this tool to pipy repo yet. Hence, its clone only for now.

### PIP

```sh
pip install openman
```

### Manual
To install, simple clone this repo

```sh
git clone https://github.com/codeasashu/openman.git
```

and install

```sh
python setup.py install
```

## Quick Start

This tool can be used as a python package or as a standalone cli.

To start, simply type `openman --help` and it will display help

```sh
Usage: openman [OPTIONS] COMMAND [ARGS]...

  Convert or mock your postman collection to openapi schema

Options:
  --help  Show this message and exit.

Commands:
  convert
  mock
```

### Convert postman to openapi spec

Easy!! Just use `convert` command (default output is yaml)

```sh
openman convert postman-collection.json spec.yaml
```

Or, you can output to json by

```sh
openman convert -f json postman-collection.json spec.yaml
```

### Mocking spec

I am using the some cherry on top of the awesome project [Connexion](https://github.com/zalando/connexion)

Basically, I am using postman example as mock responses, given the request has matching parameters (query, headers etc.). Even if they do not match, this tool gives out the mock responses for provided schema.

```sh
openman mock spec.yaml
```

### Ignore schema

Sometimes, your api responses have some data which varies. For instance, consider this response for the api `POST /user`:

```json
{
    "result": {
        "timestamp": 1572696732,
        "username": "abc",
        "tags": {
            "tag1" : "something",
            "tag3": "somethig else"
        },
        "some-changing-key": "whatever"
    }
}
```

You do want to record the `username`, `timestamp` fields, but what about `some-changing-key` field? What about fields inside `tags`? You want to keep the `tags` key as it will always be included in response, but do not want to keep `some-changing-key` as it may or maynot appear in responses.

**Sometimes you may want to ignore only the values of a key, while sometimes you want the key value pair to be ignored alltogether**

For such cases, you may not want to document them. For such purpose, **Ignore file** is used.

In ignore file, you can document the fields you want the openman to ignore. It uses the [jsonpath-rw](https://pypi.org/project/jsonpath-rw/) library and uses its syntax (which is quite easy to learn).

**To ignore only values but keep the keys**, simple use the `jsonpath-rw` syntax that points to the key. For ex- `$.result.tags.[*]` will find everything inside `tags` field in `result` object.

**To ignore both key and values**, simply use the above method, i.e. write your `jsonpath-rw` regex that matches the path, and *append* `:a` to it. For example, if you want to delete everything inside tag *including* tag field itself, you can do so by: `$.result.tags.[*]:a`


Taking above example, you want to ignore following fields:

- everything inside `tags` (ignore value but NOT the key `tags`)
- `some-changing-key` field (ignore both key and value)

You can define them in a file `ignore.yaml` as such:

```yaml
schema:
   /user:
     post:
       200:
         - '$.result.tags.[*]' //Ignore everything inside tags field
         - '$.result.some-changing-key:a' //Ignore 'some-changing-key'. Note the leading :a 
```

and then you can convert your postman collection to openapi spec without these fields:

```sh
openman -i ignore.yaml postman-collection.json spec.yaml
```

PS: Leading `:a` in jsonpath-rw syntax with ignore both the key and values, otherwise only values are ignored.

## Change spec format

The default output conversion format is `yaml`. However, you can easily change the format to json by:

```sh
openman -f json postman-collection.json spec.json
```
