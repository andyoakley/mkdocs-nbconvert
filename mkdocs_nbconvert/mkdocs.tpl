{%- extends 'classic/base.html.j2' -%}

{%- block footer -%}
<div class="nbconvert-download">
    <a href="{{ resources['filename'] }}">
        Download
        {{ resources['filename'] }}
    </a>
</div>
{% endblock footer %}