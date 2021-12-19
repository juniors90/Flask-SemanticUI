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

from flask_semantic import (
    link_css_with_sri,
    scripts_with_sri,
    simple_link_css,
    simple_scripts_js,
)


def test_link_css():
    css_html_sri = (
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/'
        + 'npm/semantic-ui@2.4.2/dist/semantic.min.css" '
        + 'integrity="sha256-UXesixbeLkB/UYxVTzuj/gg3+LMzgwAmg3zD+C4ZASQ=" '
        + 'crossorigin="anonymous">'
    )
    css_sri = "sha256-UXesixbeLkB/UYxVTzuj/gg3+LMzgwAmg3zD+C4ZASQ="
    css_url = (
        "https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css"
    )
    css = (
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm'
        + '/semantic-ui@2.4.2/dist/semantic.min.css">'
    )
    assert css == simple_link_css(css_url)
    assert css_sri in link_css_with_sri(css_url, css_sri)
    assert css_url in link_css_with_sri(css_url, css_sri)
    assert css_html_sri == link_css_with_sri(css_url, css_sri)


def test_simple_link_css_js():
    js_html_sri = (
        '<script src="https://cdn.jsdelivr.net/npm/'
        + 'semantic-ui@2.4.2/dist/semantic.min.js" '
        + 'integrity="sha256-CgSoWC9w5wNmI1aN8dIMK+6DPelUEtvDr+Bc2m/0Nx8=" '
        + 'crossorigin="anonymous"></script>'
    )
    js_sri = "sha256-CgSoWC9w5wNmI1aN8dIMK+6DPelUEtvDr+Bc2m/0Nx8="
    js_url = (
        "https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"
    )
    js = (
        '<script src="https://cdn.jsdelivr.net/'
        + 'npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>'
    )
    assert js == simple_scripts_js(js_url)
    assert js_sri in scripts_with_sri(js_url, js_sri)
    assert js_url in scripts_with_sri(js_url, js_sri)
    assert js_html_sri == scripts_with_sri(js_url, js_sri)


def test_semantic_find_local_resource(app, semantic):
    with app.app_context(), app.test_request_context():
        app.config["SEMANTIC_SERVE_LOCAL"] = True
        app.config["SERVER_NAME"] = "localhost"
        url_css = semantic.load_css()
        url_js_and_jquery = semantic.load_js()
    css = (
        '<link rel="stylesheet" type="text/css" '
        + 'href="/static/css/semantic.min.css">'
    )
    js = '<script src="/static/js/semantic/semantic.min.js"></script>'
    jquery = '<script src="/static/js/semantic/jquery.min.js"></script>'
    assert css in url_css
    assert js in url_js_and_jquery
    assert jquery in url_js_and_jquery


def test_semantic_find_cdn_resource(app, semantic):
    with app.app_context(), app.test_request_context():
        app.config["SEMANTIC_SERVE_LOCAL"] = False
        url_css = semantic.load_css()
        url_js_and_jquery = semantic.load_js()
    css = (
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/'
        + 'semantic-ui@2.4.2/dist/semantic.min.css" '
        + 'integrity="sha256-UXesixbeLkB/UYxVTzuj/gg3+LMzgwAmg3zD+C4ZASQ="'
        + ' crossorigin="anonymous">'
    )
    js = (
        '<script src="https://cdn.jsdelivr.net/npm/'
        + 'semantic-ui@2.4.2/dist/semantic.min.js" '
        + 'integrity="sha256-CgSoWC9w5wNmI1aN8dIMK+6DPelUEtvDr+Bc2m/0Nx8=" '
        + 'crossorigin="anonymous"></script>'
    )
    jquery = (
        '<script src="https://cdn.jsdelivr.net/npm/'
        + 'jquery@3.1.1/dist/jquery.min.js" '
        + 'integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8=" '
        + 'crossorigin="anonymous"></script>'
    )
    assert css in url_css
    assert js in url_js_and_jquery
    assert jquery in url_js_and_jquery
