from flask import current_app

from flask_semantic_ui import CDN_BASE

import pytest as pt


@pt.mark.usefixtures("client")
class TestSemanticUI:
    def test_extension_init(self, app):
        with app.app_context():
            extensions = current_app.extensions
        assert "semantic" in extensions
        assert "semantic_ui" not in extensions

    def test_load_css_with_default_versions(self, semantic):
        rv = semantic.load_css()
        CDN = (
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm'
            + '/semantic-ui@2.4.2/dist/semantic.min.css" integrity='
            + '"sha256-UXesixbeLkB/UYxVTzuj/gg3+LMzgwAmg3zD+C4ZASQ=" '
            + 'crossorigin="anonymous">'
        )
        semantic_css = (
            '<link rel="stylesheet" href="'
            + CDN_BASE
            + "/semantic-ui@"
            + semantic.semantic_version
            + "/dist/"
            + semantic.semantic_css_filename
            + '" integrity="'
            + semantic.semantic_css_integrity
            + '" crossorigin="anonymous">'
        )
        assert semantic_css == rv
        assert semantic_css == CDN
        assert rv == CDN


"""
    def test_load_css_with_non_default_versions(self, semantic):
        def _check_assertions(rv):
            assert 'semantic.min.css' in rv
            assert 'integrity="' not in rv
            assert 'crossorigin="anonymous"' not in rv

        rv = semantic.load_css(s_version='2.4.1')
        _check_assertions(rv)
        rv = semantic.load_css(s_version='2.4.2')
        _check_assertions(rv)
"""
