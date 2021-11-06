import re

import pytest as pt

from flask_semantic_ui import SemanticUI


@pt.fixture(autouse=True)
def semantic(app):
    yield SemanticUI(app)


@pt.fixture
def cdn_suiv():
    semantic_ui_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.semantic_version)
    ).group(1)
    return "Semantic UI - " + semantic_ui_version


@pt.fixture
def cdn_jqv():
    jquery_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.jquery_version)
    ).group(1)
    return "jQuery v" + jquery_version


@pt.fixture
def local_suiv():
    semantic_ui_version = re.search(
        r"(\d+\.\d+\.\d+)", str(SemanticUI.semantic_version)
    ).group(1)
    return "Semantic UI - " + semantic_ui_version


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
