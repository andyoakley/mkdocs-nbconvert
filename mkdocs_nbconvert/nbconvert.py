from mkdocs.plugins import BasePlugin
from mkdocs import utils
import os.path
from nbconvert import MarkdownExporter
import nbformat


class NotebookConverter(BasePlugin):

    def __init__(self):
        self.exporter = MarkdownExporter()
        if not '.ipynb' in utils.markdown_extensions:
            utils.markdown_extensions.append('.ipynb')

    def can_load(self, path):
        return path.lower().endswith('.ipynb') and not 'ipynb_checkpoints' in path.lower()

    def on_config(self, config, **kwargs):
        config['extra_javascript'].append('https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML')

    def on_page_read_source(self, something, **kwargs):
        page = kwargs['page']
        config = kwargs['config']
        input_path = page.file.src_path

        if not self.can_load(input_path):
            return
        
        ipynb_path = os.path.join(config['docs_dir'], input_path)
        nb = nbformat.read(ipynb_path, as_version=4)

        # we'll place the supporting files alongside the final HTML
        stem = os.path.join(os.path.splitext(os.path.basename(input_path))[0], '..')
        exporter_resources = {'output_files_dir': stem}
        
        (body, resources) = self.exporter.from_notebook_node(nb,
            resources=exporter_resources)
            
        # folder in site may not have been created yet, create it so that we
        # can drop the support files in there
        target_in_site = os.path.dirname(page.file.abs_dest_path)
        os.makedirs(os.path.join(target_in_site, stem), exist_ok=True)

        for output in resources['outputs'].keys():
            path = os.path.join(
                    target_in_site,
                    output
                    )

            with open(path, 'wb') as f:
                f.write(resources['outputs'][output])

        return body
