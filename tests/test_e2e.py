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


def grep(f, needle):
    with open(f, 'r') as h:
        content = h.read()
        return needle in content


def test_plain(mkdocs_site, tmpdir):
    targets = ['index.html', 'plain.ipynb']
    check_for_output(mkdocs_site, tmpdir, 'plain', targets)


def test_image(mkdocs_site, tmpdir):
    targets = [
        'index.html',
        'with-image.ipynb',
    ]
    check_for_output(mkdocs_site, tmpdir, 'with-image', targets)

    assert grep(
        os.path.join(tmpdir, 'with-image', 'index.html'),
        '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAXcAAAD8'
    )


def test_attachment(mkdocs_site, tmpdir):
    targets = [
        'index.html',
        'attachment.ipynb',
    ]
    check_for_output(mkdocs_site, tmpdir, 'attachment', targets)

    assert grep(
        os.path.join(tmpdir, 'attachment', 'index.html'),
        '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUh'
    )
