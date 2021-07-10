import os
import sys
import re
from subprocess import check_output
try:
    import mkdocs
except ImportError:
    raise ImportError('mkdocs does not appear to be installed. Install mkdocs before mkdocs-nbconvert')

def get_init_file():
    """ Get the location of the init directory
    """
    mkdoc_path = os.path.dirname(mkdocs.__file__)
    init_file = os.path.join(mkdoc_path, 'utils', '__init__.py')

    return init_file

if __name__ == '__main__':
    init_file = get_init_file()

    with open(init_file, 'r') as f:
        init_code = f.read()

    regexp = 'markdown_extensions = ([^\]]*)\]'
    search_groups = re.search(regexp, init_code)
    extension_def = search_groups.group(0)

    current_extensions = [s.strip().split(',')[0] for s in extension_def.split('\n')[1:-1]]
        
    # Make sure extension isn't present already
    new_ext = "'%s'" % '.ipynb'
    if new_ext not in current_extensions:
        current_extensions.append(new_ext)

    formatted_extensions = ['    ' + e for e in current_extensions]
    formatted_extensions = ',\n'.join(formatted_extensions)
   

    # regenerate string
    new_block= 'markdown_extensions = [\n' + formatted_extensions + '\n]'

    new_code = re.sub(regexp, new_block, init_code)

    with open(init_file, 'w') as f:
        f.write(new_code)
