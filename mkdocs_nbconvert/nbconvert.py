from mkdocs.plugins import BasePlugin
import subprocess
import os.path
import tempfile
import shutil 

class NotebookConverter(BasePlugin):

    def __init__(self):
        pass

    def on_config(self, config, **kwargs):
        config['extra_javascript'].append('https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML')

    def on_page_read_source(self, something, **kwargs):
        page = kwargs['page']
        config = kwargs['config']

        if not page.input_path.endswith('.ipynb'):
            return

        tmp = tempfile.mkdtemp()
        ipynb_path = os.path.join(config['docs_dir'], page.input_path)

        # execute nbconvert
        subprocess.check_output([
            'jupyter', 'nbconvert',
            ipynb_path, 
            '--to', 'markdown',
            '--output-dir', tmp,
            ])

        md_path = os.path.join(
                tmp,
                os.path.basename(ipynb_path.replace('.ipynb', '.md'))
                )
        
        # load md file to memory but we don't want it to be copied to the site
        # output
        with open(md_path, 'r') as mdfile:
            md = mdfile.read()
        os.remove(md_path)

        # copy any other assets
        files = os.path.join(
                tmp,
                os.path.splitext(os.path.basename(ipynb_path))[0]+'_files'
                )

        target_in_site = os.path.join(
                config['site_dir'],
                page.abs_url[1:],
                '..',
                os.path.splitext(os.path.basename(ipynb_path))[0]+'_files'
                )

        if os.path.isdir(files):
            shutil.copytree(files, target_in_site)

        # delete the temp output
        shutil.rmtree(tmp)
        
        # return md file
        return md
