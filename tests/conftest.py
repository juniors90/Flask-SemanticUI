import re

import flask
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    HiddenField,
    RadioField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length
import pytest as pt
import typing as t

import flask_semantic_ui


class ExampleForm(FlaskForm):
    name = StringField("Name")
    username = StringField(
        "Username", validators=[DataRequired(), Length(1, 20)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(8, 150)]
    )
    country_code = IntegerField("Country Code", validators=[DataRequired()])
    radio_field = RadioField(
        "This is a radio field",
        choices=[
            ("head_radio", "Head radio"),
            ("radio_76fm", "Radio '76 FM"),
            ("lips_106", "Lips 106"),
            ("wctr", "WCTR"),
        ],
    )
    hidden = HiddenField()
    remember = BooleanField("Remember me")
    submit_button = SubmitField("Submit Form")


if t.TYPE_CHECKING:
    from flask.testing import FlaskClient


@pt.fixture
def app() -> "flask.Flask":
    from flask_semantic_ui import SemanticUI

    app = flask.Flask(__name__)
    SemanticUI(app)
    app.secret_key = "for test"
    app.testing = True
    return app


@pt.fixture
def client(app: "flask.Flask") -> "FlaskClient":
    return app.test_client()


@pt.fixture
def cdn_suiv():
    semantic_ui_version = re.search(
        r"(\d+\.\d+\.\d+)", str(flask_semantic_ui.SEMANTIC_UI_VERS)
    ).group(1)
    return "Semantic UI - " + semantic_ui_version


@pt.fixture
def cdn_jqv():
    jquery_version = re.search(
        r"(\d+\.\d+\.\d+)", str(flask_semantic_ui.JQUERY_VERSION)
    ).group(1)
    return "jQuery v" + jquery_version


@pt.fixture
def local_suiv():
    semantic_ui_version = re.search(
        r"(\d+\.\d+\.\d+)", str(flask_semantic_ui.SEMANTIC_UI_LOCAL_VERSION)
    ).group(1)
    return "Semantic UI - " + semantic_ui_version


@pt.fixture
def local_jsv():
    js_version = re.search(
        r"(\d+\.\d+\.\d+)", str(flask_semantic_ui.JS_LOCAL_VERSION)
    ).group(1)
    return "Semantic UI - " + js_version


@pt.fixture
def example_form():
    return ExampleForm
