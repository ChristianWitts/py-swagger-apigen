import os
import shutil
import codecs

import yaml
import json
import click
from jinja2 import Template

PROJECT = None
TARGET = None


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


def create_base():
    if not os.path.exists(PROJECT):
        os.mkdir(PROJECT)

    # Copy requirements
    shutil.copy('templates/{}/requirements.tpl'.format(TARGET),
                '{}/requirements.txt'.format(PROJECT))
    # Copy middleware
    shutil.copy('templates/{}/middleware.tpl'.format(TARGET),
                '{}/middleware.py'.format(PROJECT))


def get_resource_name(path_spec):
    parts = path_spec.split('/')
    return '{}Resource'.format(''.join(part.title() for part in parts
                                       if part and part[0] != '{'))


def generate_validation_schemas(definitions):
    schemas = ((schema_name, json.dumps(schema_spec, indent=4))
                for schema_name, schema_spec in definitions.iteritems())

    with open('templates/{}/schemas.tpl'.format(TARGET), 'r') as s:
        template = Template(s.read())

    with open('{}/schemas.py'.format(PROJECT), 'w') as s:
        s.write(template.render(schemas=schemas))


def generate_entrypoint(routing_table):
    middlewares = ('RequireJSON', 'JSONTranslator')
    with open('templates/{}/main.tpl'.format(TARGET), 'r') as t:
        template = Template(t.read())

    with open('{}/main.py'.format(PROJECT), 'w') as f:
        f.write(template.render(routing_table=routing_table, middlewares=middlewares))


def generate_api(config):
    routing_table = []
    for path_spec, endpoints in config['paths'].iteritems():
        resource_name = get_resource_name(path_spec)
        routing_table.append((path_spec, resource_name))

    generate_entrypoint(routing_table)


def copy_ui(destination):
    if os.path.exists('{}/ui'.format(destination)):
        print "Skipping UI"
    else:
        print "Copying UI"
        shutil.copytree('templates/ui', '{}/ui'.format(destination), symlinks=False)


@click.command()
@click.argument("destination", required=True)
@click.option("-s", "--swagger", required=True, help="Swagger spec")
@click.option("-t", "--target", required=True, help="Target framework",
              type=click.Choice(["falcon", "flask"]))
@click.option("--ui", default=False, is_flag=False, help="Generate swagger UI.")
def generate(destination, swagger, target, ui=False):
    """Main entry point to generate your API based off of the swagger documentation.

    :param str destination: Your project name.
    :param str swagger: The swagger specification file.
    :param bool ui: If you want to have a swagger UI generated.
    :return: None
    """
    # Set some globals for convenience
    global PROJECT
    PROJECT = destination
    global TARGET
    TARGET = target

    spec = load_spec(swagger)
    create_base()
    if ui:
        copy_ui()
    generate_validation_schemas(spec['definitions'])
    generate_api(spec)


if __name__ == '__main__':
    generate()
