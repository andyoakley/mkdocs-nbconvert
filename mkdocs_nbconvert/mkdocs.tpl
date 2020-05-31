{% extends 'markdown.tpl' %}

{% block input %}
<div class="nb-input">
``` 
{%- if 'magics_language' in cell.metadata  -%}
    {{ cell.metadata.magics_language}}
{%- elif 'name' in nb.metadata.get('language_info', {}) -%}
    {{ nb.metadata.language_info.name }}
{%- endif %}
{{ cell.source }}
```
</div>
{% endblock input %}