#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Flask-SemanticUI Project (https://github.com/juniors90/Flask-SemanticUI/).
# Copyright (c) 2022, Ferreira Juan David
# License: MIT
# Full Text: https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =============================================================================
# TESTS
# =============================================================================


def test_can_import_package():
    import flask_semantic_ui  # noqa


def test_can_initialize_app_and_extesion():
    from flask import Flask
    from flask_semantic_ui import SemanticUI

    app = Flask(__name__)
    SemanticUI(app)
