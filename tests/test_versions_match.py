#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Flask-SemanticUI Project (https://github.com/juniors90/Flask-SemanticUI/).
# Copyright (c) 2022, Ferreira Juan David
# License: MIT
# Full Text: https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =============================================================================
# IMPORTS
# =============================================================================

import re

import requests


def test_semantic_ui_version_matches(
    app, cdn_suiv, client, local_suiv, local_jsv, cdn_jqv
):
    semantic_ui_vre = re.compile(r"Semantic UI - \d+\.\d+\.\d")
    jquery_vre = re.compile(r"jQuery v\d+\.\d+\.\d")

    # find cdn version
    cdn = app.extensions["semantic_ui"]["cdns"]["semantic_ui"]
    with app.app_context():
        cdn_url_css = "https:" + cdn.get_resource_url("semantic.css")
        cdn_url_js = "https:" + cdn.get_resource_url("semantic.js")

    cdn_jquery = app.extensions["semantic_ui"]["cdns"]["jquery"]
    with app.app_context():
        app.config["SEMANTIC_UI_CDN_FORCE_SSL"] = True
        cdn_url_jquery = "https:" + cdn_jquery.get_resource_url(
            "jquery.min.js"
        )

    css = requests.get(cdn_url_css).text
    js = requests.get(cdn_url_js).text
    jquery = requests.get(cdn_url_jquery).text
    cdn_version_css = semantic_ui_vre.search(css).group(0)
    cdn_version_js = semantic_ui_vre.search(js).group(0)
    cdn_version_jquery = jquery_vre.search(jquery).group(0)

    # find local version
    local_version_css = semantic_ui_vre.search(
        str(client.get("/static/semantic_ui/css/semantic.css").data)
    ).group(0)

    local_version_js = semantic_ui_vre.search(
        str(client.get("/static/semantic_ui/js/semantic.js").data)
    ).group(0)

    # get package version
    assert local_version_css == local_suiv
    assert local_version_js == local_jsv
    assert cdn_version_css == cdn_suiv
    assert cdn_version_js == cdn_suiv
    assert cdn_version_jquery == cdn_jqv
