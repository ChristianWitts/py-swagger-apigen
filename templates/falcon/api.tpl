import falcon
import jsonschema

# Import schemas to validate the incoming data against
import schemas


{{ name.upper() }} = {{ valid_schema }}

class {{name}}:
    {%- for method, values in methods.iteritems() %}
    def {{ method.lower() }}(self):
        pass
    {% endfor %}