{%- extends 'basic.tpl' -%}

{%- block header -%}
<div class="download-ipynb">
    <a href="{{ resources['filename'] }}">
        Download
        {{ resources['filename'] }}
    </a>
</div>
{% endblock header %}