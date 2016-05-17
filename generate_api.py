import os
import shutil
import codecs

import yaml
import json
import click
from jinja2 import Template


def load_spec(filename):
    """Load the Swagger specification and return the config

    :param str filename: The input filename for the swagger spec
    :return: Returns a dictionary representation of the Swagger spec
    :rtype: dict
    """
    _, extension = os.path.splitext(filename.lower())
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        if extension == '.json':
            return json.load(f)
        elif extension in ('.yml', '.yaml'):
            return yaml.load(f)


def create_base(destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    # Copy requirements
    shutil.copy('templates/falcon/requirements.tpl', '{}/requirements.txt'.format(destination))
    # Copy middleware
    shutil.copy('templates/falcon/middleware.tpl', '{}/middleware.py'.format(destination))


def get_resource_name(path_spec):
    parts = path_spec.split('/')
    return '{}Resource'.format(''.join(part.title() for part in parts
                                       if part and part[0] != '{'))


def generate_validation_schemas(destination, definitions):
    schemas = ((schema_name, json.dumps(schema_spec, indent=4))
                for schema_name, schema_spec in definitions.iteritems())

    with open('templates/falcon/schemas.tpl', 'r') as s:
        template = Template(s.read())

    with open('{}/schemas.py'.format(destination), 'w') as s:
        s.write(template.render(schemas=schemas))


def generate_entrypoint(destination, routing_table):
    middlewares = ('RequireJSON', 'JSONTranslator')
    with open('templates/falcon/main.tpl', 'r') as t:
        template = Template(t.read())

    with open('{}/main.py'.format(destination), 'w') as f:
        f.write(template.render(routing_table=routing_table, middlewares=middlewares))


def generate_api(destination, config):
    routing_table = []
    for path_spec, endpoints in config['paths'].iteritems():
        resource_name = get_resource_name(path_spec)
        routing_table.append((path_spec, resource_name))

    generate_entrypoint(destination, routing_table)


def copy_ui(destination):
    if os.path.exists('{}/ui'.format(destination)):
        print "Skipping UI"
    else:
        print "Copying UI"
        shutil.copytree('templates/ui', '{}/ui'.format(destination), symlinks=False)


@click.command()
@click.argument("destination", required=True)
@click.option("-s", "--swagger", required=True, help="Swagger spec")
@click.option("--ui", default=False, is_flag=False, help="Generate swagger UI.")
def generate(destination, swagger, ui=False):
    """Main entry point to generate your API based off of the swagger documentation.

    :param str destination: Your project name.
    :param str swagger: The swagger specification file.
    :param bool ui: If you want to have a swagger UI generated.
    :return: None
    """
    spec = load_spec(swagger)
    create_base(destination)
    if ui:
        copy_ui(destination)
    generate_validation_schemas(destination, spec['definitions'])
    generate_api(destination, spec)


if __name__ == '__main__':
    generate()
