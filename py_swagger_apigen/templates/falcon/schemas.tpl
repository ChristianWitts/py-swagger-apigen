{%- for schema_name, schema_spec in schemas %}
{{ schema_name.upper() }} = {{ schema_spec }}
{%- endfor %}