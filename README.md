This mkdocs plugin uses ``nbconvert`` to convert Jupyter notebooks into Markdown as they are loaded. A small patch is required that lets mkdocs invoke plugins for non-Markdown files.

# Patch
In ``utils/__init__.py`` the definition of ``markdown_extensions`` needs to include ``.ipynb``.



