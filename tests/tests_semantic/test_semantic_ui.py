#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file was part of Flask-Bootstrap and was modified under the terms of
# its BSD License. Copyright (c) 2013, Marc Brinkmann. All rights reserved.
#
# This file was part of Bootstrap-Flask and was modified under the terms of
# its MIT License. Copyright (c) 2018 Grey Li. All rights reserved.
#
# This file is part of the
#   Flask-SemanticUI Project (
#                 https://github.com/juniors90/Flask-SemanticUI/
#    ).
# Copyright (c) 2021, Ferreira Juan David
# License: MIT
# Full Text:
#    https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =====================================================================
# TESTS
# =====================================================================


from flask import current_app

from flask_semanticui import cdn_base

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
        cdn = (
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm'
            + '/semantic-ui@2.4.2/dist/semantic.min.css" integrity='
            + '"sha256-UXesixbeLkB/UYxVTzuj/gg3+LMzgwAmg3zD+C4ZASQ=" '
            + 'crossorigin="anonymous">'
        )
        semantic_css = (
            '<link rel="stylesheet" href="'
            + cdn_base
            + "/semantic-ui@"
            + semantic.semantic_version
            + "/dist/"
            + semantic.semantic_css_filename
            + '" integrity="'
            + semantic.semantic_css_integrity
            + '" crossorigin="anonymous">'
        )
        assert semantic_css == rv
        assert semantic_css == cdn
        assert rv == cdn


def test_semantic_get_sri(app, semantic):
    with app.app_context():
        app.config["SEMANTIC_SERVE_LOCAL"] = True
        assert (
            semantic._get_sri(
                name="semantic_js",
                version="2.4.2",
                sri="sha256-CgSoWC9w5wNmI1aN8dIMK+6DPelUEtvDr+Bc2m/0Nx8=",
            )
            == "sha256-CgSoWC9w5wNmI1aN8dIMK+6DPelUEtvDr+Bc2m/0Nx8="
        )
        assert (
            semantic._get_sri(name="semantic_js", version="2.4.2", sri=None)
            is None
        )
