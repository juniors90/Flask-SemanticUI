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


"""
def test_semantic_find_resource(app):
    from flask_semantic import semantic_find_resource

    with app.app_context():
        url = semantic_find_resource("semantic.js", cdn="respond.js")
    c = "//cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"
    with app.app_context():
        app.config["SEMANTIC_CDN_FORCE_SSL"] = True
        url1 = semantic_find_resource("semantic.js", cdn="respond.js")
    c1 = "https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"
    with app.app_context():
        app.config["SEMANTIC_CDN_FORCE_SSL"] = True
        url2 = semantic_find_resource(
            'jquery.js', cdn='jquery', use_minified=True
        )
    c2 = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"
    assert url == c
    assert url1 == c1
    assert url2 == c2
"""


"""
def test_semantic_find_local_resource(app):
    from flask_semantic import StaticCDN
    with app.app_context():
        app.config['SERVER_NAME'] = 'localhost'
        url = StaticCDN().get_resource_url(filename='css/semantic.css')
    c = '//cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js'
    assert url == c
"""
