
from distutils.core import setup

# Automatically edit the mkdocs/utils/__init__.py to include 
# .ipynb extensions.
from subprocess import call
call(['python', 'auto-patch.py'])

setup(
    name='mkdocs-nbconvert',
    version='0.1.0',
    author='Andy Oakley',
    author_email='ao@ao.vc',
    packages=['mkdocs_nbconvert'],
    license='LICENSE.txt',
    description='Mkdocs plugin to render Jupyter notebooks.',
    install_requires=[
        'nbconvert',
    ],

    entry_points={
        'mkdocs.plugins': [
            'nbconvert = mkdocs_nbconvert.nbconvert:NotebookConverter',
        ]
    }
)
