#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file was part of Flask-Bootstrap and was modified under the terms of
# its BSD License. Copyright (c) 2013, Marc Brinkmann. All rights reserved.
#
# This file was part of Bootstrap-Flask and was modified under the terms of
# its MIT License. Copyright (c) 2018 Grey Li. All rights reserved.
#
# This file is part of the
# Flask-SemanticUI Project (https://github.com/juniors90/Flask-SemanticUI/).
# Copyright (c) 2021, Ferreira Juan David
# License: MIT
# Full Text: https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""Flask-SemanticUI.

Implementation of SemanticUI in Flask.
"""

# =============================================================================
# META
# =============================================================================

from .core import _SemanticUI


class SemanticUI(_SemanticUI):
    """Base class for palies the SemanticUI framework.

    Initilize the extension::

        from flask import Flask
        from flask_semantic import SemantiUI

        app = Flask(__name__)
        semantic = SemanticUI(app)


    Or with the application factory::


        from flask import Flask
        from flask_semantic import SemanticUI

        Semantic = SemanticUI()

        def create_app():
            app = Flask(__name__)
            semantic.init_app(app)

    """

    jquery_version = "3.1.1"
    semantic_version = "2.4.2"
    semantic_css_integrity = (
        "sha256-UXesixbeLkB/UYxVTzuj/gg3+LMzgwAmg3zD+C4ZASQ="
    )
    semantic_js_integrity = (
        "sha256-CgSoWC9w5wNmI1aN8dIMK+6DPelUEtvDr+Bc2m/0Nx8="
    )
    jquery_integrity = "sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
    static_folder = "semantic"
