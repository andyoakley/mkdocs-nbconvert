import pytest
import os.path

from mkdocs import config
from mkdocs.commands import build


@pytest.fixture()
def mkdocs_site(tmpdir):
    mkdocs_root = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_data'
    )

    cfg = config.load_config(os.path.join(mkdocs_root, 'mkdocs.yml'))
    cfg['site_dir'] = tmpdir
    build.build(cfg)


def check_for_output(mkdocs_site, tmpdir, path, targets):
    for target in targets:
        p = os.path.join(
            tmpdir,
            path,
            target
        )
        assert os.path.exists(p)


def test_plain(mkdocs_site, tmpdir):
    targets = ['index.html', 'plain.ipynb']
    check_for_output(mkdocs_site, tmpdir, 'plain', targets)


def test_image(mkdocs_site, tmpdir):
    targets = [
        'index.html',
        'with-image.ipynb',
        'output_3_0.png'
    ]
    check_for_output(mkdocs_site, tmpdir, 'with-image', targets)
