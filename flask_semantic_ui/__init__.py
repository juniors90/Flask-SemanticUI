#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Flask-SemanticUI Project (https://github.com/juniors90/Flask-SemanticUI/).
# Copyright (c) 2022, Milagros Colazo
# License: MIT
# Full Text: https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""
Flask-SemanticUI.
Implementation of SemanticUI in Flask.
"""

# =============================================================================
# META
# =============================================================================

__version__ = "2.4.2"

# =============================================================================
# IMPORTS
# =============================================================================

import re

from flask import Blueprint, current_app, url_for

from .forms import render_form

try:
    from wtforms.fields import HiddenField
except ImportError:

    def is_hidden_field_filter(field):
        raise RuntimeError("WTForms is not installed.")


else:

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)


# =============================================================================
# CONSTANTS
# =============================================================================

S_UI_VERS = re.sub(r"^(\d+\.\d+\.\d+).*", r"\1", __version__)
JQUERY_VERSION = "3.6.0"
HTML5SHIV_VERSION = "3.7.3"
JS_VERSION = "2.4.1"


# =============================================================================
# CLASSES
# =============================================================================


class CDN(object):
    """Base class for CDN objects."""

    def get_resource_url(self, filename):
        """Return resource url for filename."""
        raise NotImplementedError


class StaticCDN(object):
    """A CDN that serves content from the local application.
        Parameters
        ----------
        static_endpoint: Endpoint to use.
        rev: If ``True``, honor ``SEMANTIC_UI_QUERYSTRING_REVVING``.
    """
    def __init__(self, static_endpoint="static", rev=False):
        self.static_endpoint = static_endpoint
        self.rev = rev

    def get_resource_url(self, filename):
        extra_args = {}

        if self.rev and current_app.config["SEMANTIC_UI_QUERYSTRING_REVVING"]:
            extra_args["semantic_ui"] = __version__

        return url_for(self.static_endpoint, filename=filename, **extra_args)


class WebCDN(object):
    def __init__(self, baseurl):
        self.baseurl = baseurl
        """Serves files from the Web.
        Parameters
        ----------
        baseurl: ``str``
            The baseurl. Filenames are simply appended to this URL.
        """

    def get_resource_url(self, filename):
        return self.baseurl + filename


class ConditionalCDN(object):
    """Serves files from one CDN or another, depending on whether a
    configuration value is set.

    :param confvar: Configuration variable to use.
    :param primary: CDN to use if the configuration variable is ``True``.
    :param fallback: CDN to use otherwise.
    """

    def __init__(self, confvar, primary, fallback):
        self.confvar = confvar
        self.primary = primary
        self.fallback = fallback

    def get_resource_url(self, filename):
        if current_app.config[self.confvar]:
            return self.primary.get_resource_url(filename)
        return self.fallback.get_resource_url(filename)


def semantic_ui_find_resource(
    filename, cdn, use_minified=None, local=True, jquery=None
):
    """Resource finding function, also available in templates.

    Tries to find a resource, will force SSL depending on
    ``SEMANTIC_UI_CDN_FORCE_SSL`` settings.

    :param filename: File to find a URL for.
    :param cdn: Name of the CDN to use.
    :param use_minified': If set to ``True``/``False``, use/don't use
                          minified. If ``None``, honors
                          ``SEMANTIC_UI_USE_MINIFIED``.
    :param local: If ``True``, uses the ``local``-CDN when
                  ``SEMANTIC_UI_SERVE_LOCAL`` is enabled. If ``False``, uses
                  the ``static``-CDN instead.
    :param jquery: For the JQuery CDN.
    :return: A URL.
    """
    config = current_app.config

    if use_minified is None:
        use_minified = config["SEMANTIC_UI_USE_MINIFIED"]

    if use_minified:
        filename = "%s.min.%s" % tuple(filename.rsplit(".", 1))

    if jquery:
        filename = ".min.js"

    cdns = current_app.extensions["semantic_ui"]["cdns"]
    resource_url = cdns[cdn].get_resource_url(filename)

    if resource_url.startswith("//") and config["SEMANTIC_UI_CDN_FORCE_SSL"]:
        resource_url = f"https:{resource_url}"

    return resource_url


class SemanticUI(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
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
        app.jinja_env.add_extension("jinja2.ext.do")

        if not hasattr(app, "extensions"):
            app.extensions = {}

        local = StaticCDN("semantic_ui.static", rev=True)
        static = StaticCDN()

        def lwrap(cdn, primary=static):
            return ConditionalCDN("SEMANTIC_UI_SERVE_LOCAL", primary, cdn)

        s = f"https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/{S_UI_VERS}/"
        semantic_ui = lwrap(
            WebCDN(
                s
            ),
            local,
        )

        jquery = lwrap(
            WebCDN(f"https://code.jquery.com/jquery-{JQUERY_VERSION}")
        )
        h = f"//cdnjs.cloudflare.com/ajax/libs/html5shiv/{HTML5SHIV_VERSION}/"
        html5shiv = lwrap(
            WebCDN(
                h
            )
        )
        j = f"https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/{JS_VERSION}"
        respondjs = lwrap(WebCDN(j), local,)

        app.extensions["semantic_ui"] = {
            "cdns": {
                "local": local,
                "static": static,
                "semantic_ui": semantic_ui,
                "jquery": jquery,
                "html5shiv": html5shiv,
                "respond.js": respondjs,
            },
        }

        # setup support for flask-nav
        renderers = app.extensions.setdefault("nav_renderers", {})
        renderer_name = (__name__ + ".nav", "SemanticUIRenderer")
        renderers["semantic_ui"] = renderer_name

        # make semantic ui the default renderer
        renderers[None] = renderer_name
