import falcon
import jsonschema

# Import schemas to validate the incoming data against
import schemas


{%- for resource, methods in resources %}
class {{ resource }}:
    {%- for method, parameters in methods %}

    def on_{{ method.lower() }}(self, req, resp{{ parameters.__len__() and ', ' or ''}}{{ parameters | join(', ')}}):
        pass
    {% endfor %}


{%- endfor %}

