import falcon
import jsonschema

# Import schemas to validate the incoming data against
import schemas

{% for resource, methods in resources %}
class {{ resource }}:
    {%- for method, parameters, required, body_schema in methods %}
    def on_{{ method.lower() }}(self, req, resp{{ parameters.__len__() and ', ' or ''}}{{ parameters | join(', ')}}):
        {%- for r in required %}
        if not {{ r }}:
            raise falcon.HTTPError(falcon.HTTP_400, "{{ r }} is required.")
        {%- endfor %}

        {%- if method == 'post' %}
        try:
            doc = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest("Missing request body",
                                        "The parameters must be submitted in the address body")
        {%- if body_schema %}
        try:
            jsonschema.validate(doc, schemas.{{ body_schema }})
        except jsonschema.ValidationError, e:
            raise falcon.HTTPBadRequest("Validation failed for request body",
                                        "{} - {}".format(e.relative_path[0],
                                                         e.message))
        {%- endif %}
        {%- endif %}

        resp.status = falcon.HTTP_200
        resp.body = ''

    {% endfor %}
{%- endfor %}
