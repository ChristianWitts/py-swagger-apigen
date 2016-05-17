import falcon

import api
import middleware

app = application = falcon.API(middleware=[
{%- for middleware in middlewares %}
    middleware.{{ middleware }}(),
{%- endfor %}
])

{%- for route, resource in routing_table %}
app.add_route("{{ route }}", api.{{ resource }}())
{%- endfor %}
