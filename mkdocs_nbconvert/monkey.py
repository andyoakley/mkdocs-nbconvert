import os
from mkdocs.structure.files import File

# monkeypatch the is_documentation_page method in mkdocs itself
# so that this plugin will actually get called when notebooks are
# processed

original_is_documentation_page = File.is_documentation_page

def my_is_documentation_page(self):
    md = original_is_documentation_page(self)
    ipynb = os.path.splitext(self.src_path)[1] == '.ipynb' and not 'ipynb_checkpoints' in self.src_path
    return md or ipynb

File.is_documentation_page = my_is_documentation_page


