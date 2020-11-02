from mkdocs import utils
from mkdocs.plugins import BasePlugin
import os
import os.path
from nbconvert import HTMLExporter
import nbformat
import pkgutil
import tempfile


class NotebookConverter(BasePlugin):

    def __init__(self):
        if '.ipynb' not in utils.markdown_extensions:
            utils.markdown_extensions.append('.ipynb')

    def can_load(self, path):
        return (
            path.lower().endswith('.ipynb')
            and 'ipynb_checkpoints' not in path.lower()
        )

    def on_config(self, config, **kwargs):
        js = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.0.5/es5/startup.js'
        config['extra_javascript'].append(js)

    def on_pre_build(self, config):
        # we need to put a copy of the template file on disk
        # so that nbconvert can find it
        self.template_file = tempfile.NamedTemporaryFile(delete=False)
        tpl = pkgutil.get_data(__package__, 'mkdocs.tpl')
        self.template_file.write(tpl)
        self.template_file.flush()

    def on_post_build(self, config):
        # clean up temporary template file
        os.remove(self.template_file.name)
        self.template_file = None

    def on_page_read_source(self, page, config):
        if not self.can_load(page.file.abs_src_path):
            return
        # we'll fill this in later in on_page_content
        return ""

    def on_page_content(self, content, page, config, files):
        if not self.can_load(page.file.abs_src_path):
            return content

        exp = HTMLExporter()

        exp.template_file = self.template_file.name
        ipynb_path = page.file.abs_src_path
        nb = nbformat.read(ipynb_path, as_version=4)

        exporter_resources = {
            'filename': os.path.split(page.file.abs_src_path)[1],
        }
        (body, resources) = exp.from_notebook_node(
            nb,
            resources=exporter_resources
        )

        # copy the notebook itself into the destination too
        nb_name = os.path.split(page.file.abs_src_path)[1]
        b = os.path.join(os.path.split(page.file.abs_dest_path)[0], nb_name)
        utils.copy_file(ipynb_path, b)

        return body
