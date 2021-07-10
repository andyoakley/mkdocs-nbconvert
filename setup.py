
from distutils.core import setup

# Automatically edit the mkdocs/utils/__init__.py to include 
# .ipynb extensions.
from subprocess import call
call(['python', 'auto-patch.py'])

setup(
    name='mkdocs-nbconvert',
    version='0.2.0',
    author='Andy Oakley',
    author_email='ao@ao.vc',
    packages=['mkdocs_nbconvert'],
    package_data={"": ["*.tpl"]},
    license='LICENSE.txt',
    description='Mkdocs plugin to render Jupyter notebooks.',
    install_requires=[
        'nbconvert==5.6.1',
    ],

    entry_points={
        'mkdocs.plugins': [
            'nbconvert = mkdocs_nbconvert.nbconvert:NotebookConverter',
        ]
    }
)
