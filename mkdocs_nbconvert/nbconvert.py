from mkdocs import utils
from mkdocs.plugins import BasePlugin
from mkdocs import utils
import os.path
from nbconvert import MarkdownExporter 
import nbformat
import pkgutil
import tempfile


class NotebookConverter(BasePlugin):

    def __init__(self):
        self.exporter = MarkdownExporter()
        if not '.ipynb' in utils.markdown_extensions:
            utils.markdown_extensions.append('.ipynb')

    def can_load(self, path):
        return path.lower().endswith('.ipynb') and not 'ipynb_checkpoints' in path.lower()

    def on_config(self, config, **kwargs):
        config['extra_javascript'].append('https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML')

    def on_pre_build(self, config):
        # we need to put a copy of the template file on disk
        # so that nbconvert can find it
        self.template_file = tempfile.NamedTemporaryFile()
        tpl = pkgutil.get_data(__package__, 'mkdocs.tpl')
        self.template_file.write(tpl)
        self.template_file.flush()

    def on_post_build(self, config):
        # clean up temporary template file
        self.template_file = None

    def on_page_read_source(self, page, config):
        if not self.can_load(page.file.abs_src_path):
            return

        ipynb_path = page.file.abs_src_path
        nb = nbformat.read(ipynb_path, as_version=4)

        # we'll place the supporting files alongside the final HTML
        self.exporter.template_file = self.template_file.name
        exporter_resources = {
            'output_files_dir': '.',
        } 

        # actually do the conversion 
        (body, resources) = self.exporter.from_notebook_node(nb, resources=exporter_resources)
        
        # folder in site may not have been created yet, create it so that we
        # can drop the support files in there
        target_in_site = os.path.split(page.file.abs_dest_path)[0]
        os.makedirs(target_in_site, exist_ok=True)

        for output in resources['outputs'].keys():
            path = os.path.join(target_in_site, output)
            with open(path, 'wb') as f:
                f.write(resources['outputs'][output])

        # copy the notebook itself into the destination too
        nb_name = os.path.split(page.file.abs_src_path)[1]
        b = os.path.join(os.path.split(page.file.abs_dest_path)[0], nb_name)
        utils.copy_file(ipynb_path, b)

        # append a link to the notebook in the rendered page
        body += f'<a href="{os.path.split(page.file.abs_src_path)[1]}">Download {nb_name}</a>'

        return body
