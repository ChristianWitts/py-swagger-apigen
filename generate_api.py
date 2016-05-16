import os
import shutil

import yaml
import json
import click


def load_spec(filename):
    """Load the Swagger specification and return the config

    :param str filename: The input filename for the swagger spec
    :return: Returns a dictionary representation of the Swagger spec
    :rtype: dict
    """
    _, extension = os.path.splitext(filename.lower())
    with open(filename, 'r', encoding='utf-8') as f:
        if extension == '.json':
            return json.load(f)
        elif extension in ('.yml', '.yaml'):
            return yaml.load(f)


def create_base(destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    # Copy requirements
    shutil.copy('templates/requirements.txt', '{}/requirements.txt'.format(destination))
    # Copy middleware
    shutil.copy('templates/middleware.py', '{}/middleware.py'.format(destination))


@click.command()
@click.argument("destination", required=True)
@click.option("-s", "--swagger", required=True, help="Swagger spec")
@click.option("--ui", default=False, is_flag=False, help="Generate swagger UI.")
def generate(destination, swagger, ui=False):
    spec = load_spec(swagger)
    create_base(destination)


if __name__ == '__main__':
    generate()
