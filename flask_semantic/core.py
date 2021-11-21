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
# DOCS
# =====================================================================

import warnings

from flask import current_app, Markup, Blueprint, url_for

try:  # pragma: no cover
    from wtforms.fields import HiddenField
except ImportError:

    def is_hidden_field_filter(field):
        raise RuntimeError("WTForms is not installed.")


else:

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)


CDN_BASE = "https://cdn.jsdelivr.net/npm"


def raise_helper(message):  # pragma: no cover
    raise RuntimeError(message)


def get_table_titles(data, primary_key, primary_key_title):
    """Detect and build the table titles tuple from ORM object.

    .. note::
        Currently only support SQLAlchemy.
    """
    if not data:
        return []
    titles = []
    for k in data[0].__table__.columns.keys():
        if not k.startswith("_"):
            titles.append((k, k.replace("_", " ").title()))
    titles[0] = (primary_key, primary_key_title)
    return titles


def link_css_with_sri(url, sri):
    html = (
        f'<link rel="stylesheet" href="{url}" integrity="{sri}" '
        + 'crossorigin="anonymous">'
    )
    return html


def simple_link_css(url):
    return f'<link rel="stylesheet" href="{url}">'


def scripts_with_sri(url, sri):
    tag = (
        f'<script src="{url}" integrity="{sri}" '
        + 'crossorigin="anonymous"></script>'
    )
    return tag


def simple_scripts_js(url):
    return f'<script src="{url}"></script>'


class _SemanticUI(object):
    """Base extension class for different Semantic UI versions.

    .. versionadded:: 0.0.1
    """

    semantic_version = None
    jquery_version = None
    semantic_css_integrity = None
    semantic_js_integrity = None
    jquery_integrity = None
    static_folder = None
    semantic_css_filename = "semantic.min.css"
    semantic_js_filename = "semantic.min.js"
    jquery_filename = "jquery.min.js"

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Application factory."""

        # default settings
        app.config.setdefault("SEMANTIC_SERVE_LOCAL", False)
        app.config.setdefault("SEMANTIC_BUTTON_STYLE", "primary")
        app.config.setdefault("SEMANTIC_BUTTON_SUBMIT_STYLE", "default")
        app.config.setdefault("SEMANTIC_BUTTON_SIZE", None)
        app.config.setdefault("SEMANTIC_BUTTON_SUBMIT_SIZE", None)
        app.config.setdefault("SEMANTIC_ICON_TYPE", None)
        app.config.setdefault("SEMANTIC_ICON_COLOR", None)
        app.config.setdefault(
            "SEMANTIC_MSG_CATEGORY", None
        )  # change primary by None
        app.config.setdefault("SEMANTIC_TABLE_VIEW_TITLE", "View")
        app.config.setdefault("SEMANTIC_TABLE_EDIT_TITLE", "Edit")
        app.config.setdefault("SEMANTIC_TABLE_DELETE_TITLE", "Delete")
        app.config.setdefault("SEMANTIC_TABLE_NEW_TITLE", "New")
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["semantic"] = self

        blueprint = Blueprint(
            "semantic",
            __name__,
            static_folder=f"static/{self.static_folder}",
            static_url_path=f"{app.static_url_path}",
            template_folder="templates",
        )

        app.register_blueprint(blueprint)

        app.jinja_env.globals["semantic"] = self
        app.jinja_env.globals[
            "semantic_is_hidden_field"
        ] = is_hidden_field_filter
        app.jinja_env.globals["get_table_titles"] = get_table_titles
        app.jinja_env.globals["warn"] = warnings.warn
        app.jinja_env.globals["raise"] = raise_helper
        app.jinja_env.add_extension("jinja2.ext.do")

    def load_css(self, s_version=None, semantic_sri=None):
        """Load Semantic's css resources with given version.

        Parameters
        ----------
        s_version: ``str``
            The version of Semantic UI.
        semantic_sri: ``str``
            Subresource Integrity.
        Return
        ------
            Semantic-ui CDN File.
        """

        serve_local = current_app.config["SEMANTIC_SERVE_LOCAL"]
        s_version = self.semantic_version if s_version is None else s_version
        semantic_sri = self._get_sri("semantic_css", s_version, semantic_sri)

        if serve_local:
            base_path = "css"
            url = url_for(
                "semantic.static",
                filename=f"{base_path}/{self.semantic_css_filename}",
            )
        else:
            base_path = CDN_BASE + f"/semantic-ui@{s_version}/dist/"
            url = base_path + self.semantic_css_filename

        if semantic_sri:
            css = link_css_with_sri(url, semantic_sri)
        else:
            css = f'<link rel="stylesheet" type="text/css" href="{url}">'
        return Markup(css)

    def _get_js_script(self, version, name, sri):
        """Get <script> tag for JavaScipt resources."""
        serve_local = current_app.config["SEMANTIC_SERVE_LOCAL"]
        paths = {
            "semantic-ui": f"{self.semantic_js_filename}",
            "jquery": f"{self.jquery_filename}",
        }

        if serve_local:
            base_path = "js/semantic"
            url = url_for(
                "semantic.static", filename=f"{base_path}/{paths[name]}"
            )
        else:
            url = CDN_BASE + f"/{name}@{version}/dist/{paths[name]}"

        if sri:
            script_html = scripts_with_sri(url, sri)
        else:
            script_html = simple_scripts_js(url)
        return script_html

    def _get_sri(self, name, version, sri):
        serve_local = current_app.config["SEMANTIC_SERVE_LOCAL"]

        sris = {
            "semantic_css": self.semantic_css_integrity,
            "semantic_js": self.semantic_js_integrity,
            "jquery": self.jquery_integrity,
        }

        versions = {
            "semantic_css": self.semantic_version,
            "semantic_js": self.semantic_version,
            "jquery": self.jquery_version,
        }

        if sri is not None:
            return sri
        if version == versions[name] and serve_local is False:
            return sris[name]
        return None

    def load_js(
        self,
        version=None,
        jq_version=None,  # noqa: C901
        semantic_sri=None,
        jquery_sri=None,
    ):
        """Load Seomantic UI and other resources with given version.

        Parameter
        ---------
        version: ``str``
            The version of Semantic UI.
        jq_version: ``str``
            The version of jQuery (for Semantic UI).
        semantic_sri: ``str``
            Subresource Integrity for Semantic UI..
        jquery_sri: ``str``
            Subresource Integrity for jQuery.
        Return
        ------
            Semantic-ui CDN File.
        """

        version = self.semantic_version if version is None else version
        jq_version = self.jquery_version if jq_version is None else jq_version
        sui_sri = self._get_sri("semantic_js", version, semantic_sri)
        sui_js = self._get_js_script(version, "semantic-ui", sui_sri)
        jquery_sri = self._get_sri("jquery", jq_version, jquery_sri)
        jquery = self._get_js_script(jq_version, "jquery", jquery_sri)
        return Markup(
            f"""{jquery}
            {sui_js}"""
        )
