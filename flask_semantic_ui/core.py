#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file was part of Flask-Bootstrap and was modified under the terms of
# its BSD License. Copyright (c) 2013, Marc Brinkmann. All rights reserved.
#
# This file is part of the
# Flask-SemanticUI Project (https://github.com/juniors90/Flask-SemanticUI/).
# Copyright (c) 2022, Ferreira Juan David
# License: MIT
# Full Text: https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""Flask-SemanticUI.

Implementation of SemanticUI in Flask.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import re
import warnings

import attr
from flask import Blueprint, current_app, url_for

from .forms import render_form

try:
    from wtforms.fields import HiddenField
except ImportError:

    def is_hidden_field_filter(field):  # noqa
        raise RuntimeError("WTForms is not installed.")


else:

    def is_hidden_field_filter(field):  # noqa
        return isinstance(field, HiddenField)


# =============================================================================
# CONSTANTS
# =============================================================================
ABANDONED_VERSION = "2.4.2"
SEMANTIC_UI_VERS = re.sub(r"^(\d+\.\d+\.\d+).*", r"\1", ABANDONED_VERSION)
SEMANTIC_UI_LOCAL_VERSION = "2.4.0"
JQUERY_VERSION = "3.6.0"
JS_VERSION = "2.4.2"
JS_LOCAL_VERSION = "2.4.1"


# =============================================================================
# FUNCTIONS
# =============================================================================


def semantic_ui_find_resource(
    filename, cdn, use_minified=None, local=True, jquery=None
):
    """Resource finding function, also available in templates.

    Tries to find a resource, will force SSL depending on
    ``SEMANTIC_UI_CDN_FORCE_SSL`` settings.

    Parameters
    ----------
    filename: ``str``
        File to find a URL for.
    cdn: ``str``
        Name of the CDN to use.
    use_minified: ``str``
                    If set to ``True``/``False``, use/don't use
                          minified. If ``None``, honors
                          ``SEMANTIC_UI_USE_MINIFIED``.
    local: ``bool``
            If ``True``, uses the ``local``-CDN when
                  ``SEMANTIC_UI_SERVE_LOCAL`` is enabled. If ``False``, uses
                  the ``static``-CDN instead.
    jquery: ``str``
        For the JQuery CDN.
    Return
    ------
        A URL.
    """
    config = current_app.config

    if use_minified is None:
        use_minified = config["SEMANTIC_UI_USE_MINIFIED"]

    if use_minified:
        list_file = list(filename.rsplit(".", 1))
        filename = list_file[0] + ".min." + list_file[1]

    cdns = current_app.extensions["semantic_ui"]["cdns"]
    resource_url = cdns[cdn].get_resource_url(filename)

    if resource_url.startswith("//") and config["SEMANTIC_UI_CDN_FORCE_SSL"]:
        resource_url = "https:" + resource_url

    return resource_url


# def raise_helper(message):  # noqa
#    raise RuntimeError(message)


# def get_sui_table_titles(data, primary_key, primary_key_title):
#    """Detect and build the table titles tuple from ORM object.
#
#    .. note::
#        Currently only support SQLAlchemy.
#    """
#    if not data:
#        return []
#    titles = []
#    for k in data[0].__table__.columns.keys():
#        if not k.startswith("_"):
#            titles.append((k, k.replace("_", " ").title()))
#    titles[0] = (primary_key, primary_key_title)
#    return titles


# =============================================================================
# CLASSES
# =============================================================================


# @attr.s
# class CDN(object):
#    """Base class for CDN objects."""
#
#    def get_resource_url(self, filename):
#        """Return resource url for filename."""
#        raise NotImplementedError


@attr.s(repr=False)
class StaticCDN(object):
    """A CDN that serves content from the local application.

    Attributes
    ----------
    static_endpoint: ``str``
        Endpoint to use.
    rev: ``bool``
        If ``True``, honor ``SEMANTIC_UI_QUERYSTRING_REVVING``.
    """

    static_endpoint = attr.ib(
        default="static", validator=attr.validators.instance_of(str)
    )
    rev = attr.ib(default=False, validator=attr.validators.instance_of(bool))

    def get_resource_url(self, filename):  # noqa: D202
        """Implement an inmutable dict-like to store the metadata.

        Get a resource from a url depending of filename.

        Parameters
        ----------
        filename: ``str``
            A filename to resorce that requires.
        Return
        ------
        Redirect to URL dependig od filename.
        """

        extra_args = {}

        if self.rev and current_app.config["SEMANTIC_UI_QUERYSTRING_REVVING"]:
            extra_args["semantic_ui"] = ABANDONED_VERSION

        return url_for(self.static_endpoint, filename=filename, **extra_args)


@attr.s(repr=False)
class WebCDN(object):
    """Serves files from the Web.

    Attributes
    ----------
    baseurl: ``str``
            The baseurl. Filenames are simply appended to this URL.
    """

    baseurl = attr.ib(validator=attr.validators.instance_of(str))

    def get_resource_url(self, filename):
        """Get a resource from a url depending of filename.

        Parameters
        ----------
        filename: ``str``
                    A filename to resorce that requires.
        Return
        ------
            The baseurl. Filenames are simply appended to this URL.
        """
        return self.baseurl + filename


@attr.s(repr=False)
class ConditionalCDN(object):
    """Serves files from one CDN or another.

    Depending on whether a configuration value is set.

    Attributes
    ----------
    confvar: ``str``
        Configuration variable to use.
    primary: ``str``
        CDN to use if the configuration variable is ``True``.
    fallback: ``str``
        CDN to use otherwise.
    """

    confvar = attr.ib(validator=attr.validators.instance_of(str))
    primary = attr.ib(validator=attr.validators.instance_of(StaticCDN))
    fallback = attr.ib(validator=attr.validators.instance_of(WebCDN))

    def get_resource_url(self, filename):  # noqa: D202
        """Get a resource from a url depending of filename.

        Parameters
        ----------
        filename: ``str``
            A filename to resorce that requires.
        Return
        ------
            The baseurl. Filenames are simply appended to this URL.
        """

        if current_app.config[self.confvar]:
            return self.primary.get_resource_url(filename)

        baseurl = self.fallback.get_resource_url(filename)

        return baseurl


class SemanticUI(object):
    """Define the extension class to which we can apply Semantic UI.


    .. code-block:: python
        :caption: Initilize the extension
        :linenos:

        from flask import Flask
        from flask_semantic_ui import SemanticUI
        app = Flask(__name__)
        semantic = SemanticUI(app)

    .. code-block:: python
        :caption: With the application factory
        :linenos:

        from flask import Flask
        from flask_semantic_ui import SemanticUI
        semantic = SemanticUI()

        def create_app():
            app = Flask(__name__)
            semantic.init_app(app)
    """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Application factory."""
        # default settings
        app.config.setdefault("SEMANTIC_UI_USE_MINIFIED", True)
        app.config.setdefault("SEMANTIC_UI_CDN_FORCE_SSL", False)

        app.config.setdefault("SEMANTIC_UI_QUERYSTRING_REVVING", True)
        app.config.setdefault("SEMANTIC_UI_SERVE_LOCAL", False)

        app.config.setdefault("SEMANTIC_UI_LOCAL_SUBDOMAIN", None)

        blueprint = Blueprint(
            "semantic_ui",
            __name__,
            template_folder="templates",
            static_folder="static",
            static_url_path=app.static_url_path + "/semantic_ui",
            subdomain=app.config["SEMANTIC_UI_LOCAL_SUBDOMAIN"],
        )

        # add the form rendering template filter
        blueprint.add_app_template_filter(render_form)

        app.register_blueprint(blueprint)

        app.jinja_env.globals[
            "semantic_ui_is_hidden_field"
        ] = is_hidden_field_filter
        app.jinja_env.globals[
            "semantic_ui_find_resource"
        ] = semantic_ui_find_resource
        # app.jinja_env.globals["get_sui_table_titles"] = get_sui_table_titles
        app.jinja_env.globals["warn"] = warnings.warn
        # app.jinja_env.globals["raise"] = raise_helper
        app.jinja_env.add_extension("jinja2.ext.do")

        if not hasattr(app, "extensions"):
            app.extensions = {}

        local = StaticCDN("semantic_ui.static", rev=True)
        static = StaticCDN()

        def lwrap(cdn, primary=static):
            return ConditionalCDN("SEMANTIC_UI_SERVE_LOCAL", primary, cdn)

        semantic_ui = lwrap(
            WebCDN(
                f"//cdn.jsdelivr.net/npm/semantic-ui@{SEMANTIC_UI_VERS}/dist/"
            ),
            local
        )

        respondjs = lwrap(
            WebCDN(f"//cdn.jsdelivr.net/npm/semantic-ui@{JS_VERSION}/dist/"),
            local
        )

        jquery = lwrap(
            WebCDN(
                f"//cdnjs.cloudflare.com/ajax/libs/jquery/{JQUERY_VERSION}/"
            ),
            local
        )

        app.extensions["semantic_ui"] = {
            "cdns": {
                "local": local,
                "static": static,
                "semantic_ui": semantic_ui,
                "jquery": jquery,
                "respond.js": respondjs,
            },
        }

        # setup support for flask-nav
        renderers = app.extensions.setdefault("nav_renderers", {})
        renderer_name = (__name__ + ".nav", "SemanticUIRenderer")
        renderers["semantic_ui"] = renderer_name

        # make semantic ui the default renderer
        renderers[None] = renderer_name


# 33-35, 97, 109, 118-125, 139, 173-178, 240, 314
