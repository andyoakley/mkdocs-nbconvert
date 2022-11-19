
from distutils.core import setup

setup(
    name='mkdocs-nbconvert',
    version='0.3.0',
    author='Andy Oakley',
    author_email='andy@andyoakley.com',
    packages=['mkdocs_nbconvert'],
    package_data={"": ["*.tpl"]},
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
