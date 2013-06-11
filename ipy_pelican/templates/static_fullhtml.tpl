{%- extends 'fullhtml.tpl' -%}

{% block data_png %}
{% if output.key_png %}
<img src="{{output.key_png}}">
{% else %}
<img src="data:image/png;base64,{{output.png}}">
{% endif %}
{%- endblock data_png %}
