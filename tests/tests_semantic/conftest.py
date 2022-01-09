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

import re

from flask_semanticui import SemanticUI

import pytest as pt


@pt.fixture(autouse=True)
def semantic(app):
    yield SemanticUI(app)


@pt.fixture
def cdn_suiv():
    semantic_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.semantic_version)
    ).group(1)
    return "Semantic UI - " + semantic_version


@pt.fixture
def cdn_jqv():
    jquery_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.jquery_version)
    ).group(1)
    return "jQuery v" + jquery_version


@pt.fixture
def local_suiv():
    semantic_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.semantic_version)
    ).group(1)
    return "Semantic UI - " + semantic_version


@pt.fixture
def local_jsv():
    js_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.semantic_version)
    ).group(1)
    return "Semantic UI - " + js_version


@pt.fixture
def local_jqv():
    jq_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.jquery_version)
    ).group(1)
    return "jQuery v" + jq_version
