import flask
from flask import render_template_string
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
def example_form():
    return ExampleForm


@pt.fixture(autouse=True)
def app() -> "flask.Flask":
    app = flask.Flask(__name__)
    app.secret_key = "for test"
    app.testing = True

    @app.route("/")
    def index():
        return render_template_string(
            "{{ semantic.load_css() }}{{ semantic.load_js() }}"
        )

    yield app
    # return app


@pt.fixture
def client(app: "flask.Flask") -> "FlaskClient":
    context = app.test_request_context()
    context.push()

    with app.test_client() as client:
        yield client

    context.pop()
    # return app.test_client()
