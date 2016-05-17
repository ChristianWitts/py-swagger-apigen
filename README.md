# py-swagger-apigen
An API code generator from swagger specifications.

### Current targets
* [falcon](http://falconframework.org/)

### To Do
* [flask](https://github.com/pallets/flask)

### Installation

```
git clone git@github.com:ChristianWitts/py-swagger-apigen.git
cd py-swagger-apigen
python setup.py install
```

### Command Options

```
  -s, --swagger TEXT           Swagger spec  [required]
  -t, --target [falcon|flask]  Target framework  [required]
  --ui TEXT                    Generate swagger UI.
  --help                       Show this message and exit.
```

### Examples

```
$ py-swagger-apigen --swagger petstore.json --target falcon test
$ tree test
test
├── api.py
├── main.py
├── middleware.py
├── requirements.txt
└── schemas.py
$ gunicorn -b 127.0.0.1:8001 main:application
```

### Reasoning

To speed up development of basic RESTful APIs, why not generate them from a [swagger](http://swagger.io/) specification.

### Dependencies
* [click](https://github.com/pallets/click)
* [PyYAML](http://pyyaml.org/wiki/PyYAML)
* [Jinja2](https://github.com/pallets/jinja)

### Inspiration

Inspired by the [swagger-py-codegen](https://github.com/guokr/swagger-py-codegen) and [serve_swagger](https://github.com/crowdwave/serve_swagger) projects.
