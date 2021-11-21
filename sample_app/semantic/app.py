# -*- coding: utf-8 -*-
import os
import pathlib
import sys

from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    flash,
    Markup,
)
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    PasswordField,
    IntegerField,
    TextField,
    FormField,
    SelectField,
    FieldList,
)
from wtforms.fields import (
    DateField,
    DateTimeField,
    FileField,
    RadioField,
    SelectMultipleField,
    TextAreaField,
    HiddenField,
)
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy

# this path is pointing to project/docs/source
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
FLASK_SEMANTIC_PATH = CURRENT_PATH.parent.parent

sys.path.insert(0, str(FLASK_SEMANTIC_PATH))

from flask_semantic import SemanticUI  # noqa

app = Flask(__name__)
# app.secret_key = 'dev'
app.config["SECRET_KEY"] = "secret key"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

# set default button sytle and size, will be overwritten by macro parameters
app.config["SEMANTIC_BUTTON_STYLE"] = "primary"
app.config["SEMANTIC_BUTTON_SIZE"] = ""

# set default icon title of table actions
app.config["SEMANTIC_TABLE_VIEW_TITLE"] = "Read"
app.config["SEMANTIC_TABLE_EDIT_TITLE"] = "Update"
app.config["SEMANTIC_TABLE_DELETE_TITLE"] = "Remove"
app.config["SEMANTIC_TABLE_NEW_TITLE"] = "Create"

semantic = SemanticUI(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


class ExampleForm(FlaskForm):
    """An example for semantic style form fields."""

    date = DateField(
        description="We'll never share your email with anyone else."
    )  # add help text with `description`
    datetime = DateTimeField(
        render_kw={"placeholder": "this is placeholder"}
    )  # add HTML attribute with `render_kw`
    image = FileField(render_kw={"class": "my-class"})  # add your class
    option = RadioField(
        choices=[
            ("dog", "Dog"),
            ("cat", "Cat"),
            ("bird", "Bird"),
            ("alien", "Alien"),
        ]
    )
    select = SelectField(
        choices=[
            ("dog", "Dog"),
            ("cat", "Cat"),
            ("bird", "Bird"),
            ("alien", "Alien"),
        ]
    )
    selectmulti = SelectMultipleField(
        choices=[
            ("dog", "Dog"),
            ("cat", "Cat"),
            ("bird", "Bird"),
            ("alien", "Alien"),
        ]
    )
    bio = TextAreaField()
    title = StringField()
    secret = PasswordField()
    submit = SubmitField()  # before the remember me
    remember = BooleanField("Remember me")


class HelloForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(1, 20)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(8, 150)]
    )
    submit = SubmitField()
    remember = BooleanField("Remember me")


class ButtonForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(1, 20)]
    )
    submit = SubmitField()
    delete = SubmitField()
    cancel = SubmitField()


class TelephoneForm(FlaskForm):
    country_code = IntegerField("Country Code")
    area_code = IntegerField("Area Code/Exchange")
    number = TextField("Number")


class IMForm(FlaskForm):
    protocol = SelectField(choices=[("aim", "AIM"), ("msn", "MSN")])
    username = TextField()


class ContactForm(FlaskForm):
    first_name = TextField()
    last_name = TextField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)
    emails = FieldList(TextField("Email"), min_entries=3)
    im_accounts = FieldList(FormField(IMForm), min_entries=2)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    create_time = db.Column(db.Integer, nullable=False, unique=True)


@app.before_first_request
def before_first_request_func():
    db.drop_all()
    db.create_all()
    for i in range(20):
        m = Message(
            text=f"Test message {i+1}",
            author=f"Author {i+1}",
            category=f"Category {i+1}",
            create_time=4321 * (i + 1),
        )
        if i % 4:
            m.draft = True
        db.session.add(m)
    db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form", methods=["GET", "POST"])
def test_form():
    form = HelloForm()
    return render_template(
        "form.html",
        form=form,
        telephone_form=TelephoneForm(),
        contact_form=ContactForm(),
        im_form=IMForm(),
        button_form=ButtonForm(),
        example_form=ExampleForm(),
    )


@app.route("/nav", methods=["GET", "POST"])
def test_nav():
    form = ContactForm()
    return render_template("nav.html", form=form)


@app.route("/pagination", methods=["GET", "POST"])
def test_pagination():
    page = request.args.get("page", 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items
    return render_template(
        "pagination.html", pagination=pagination, messages=messages
    )


@app.route("/flash", methods=["GET", "POST"])
def test_flash():
    flash("A simple default alert—check it out!")
    flash("A simple primary alert—check it out!", "primary")
    flash("A simple secondary alert—check it out!", "secondary")
    flash("A simple success alert—check it out!", "success")
    flash("A simple danger alert—check it out!", "danger")
    flash("A simple warning alert—check it out!", "warning")
    flash("A simple info alert—check it out!", "info")
    flash("A simple light alert—check it out!", "light")
    flash("A simple dark alert—check it out!", "dark")
    flash(
        Markup(
            '<div class="ui possitive message">'
            + '<i class="close icon"></i>'
            + '<div class="header">'
            + "A success message"
            + "</div>"
            + '<p>A simple success alert with <a href="#" class="ui item">'
            + " an example link</a>. Give it a click if you like.</p>"
            "</div>"
        ),
        "success",
    )
    return render_template("flash.html")


@app.route("/table")
def test_table():
    page = request.args.get("page", 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items
    titles = [
        ("id", "#"),
        ("text", "Message"),
        ("author", "Author"),
        ("category", "Category"),
        ("draft", "Draft"),
        ("create_time", "Create Time"),
    ]
    return render_template(
        "table.html", messages=messages, titles=titles, Message=Message
    )


@app.route("/table/<int:message_id>/view")
def view_message(message_id):
    message = Message.query.get(message_id)
    not_exist_msg = (
        f"Could not view message {message_id}"
        + " as it does not exist. Return to "
        + '<a href="/table">table</a>.'
    )
    exist_msg = (
        f"Viewing {message_id}"
        + ' with text "{message.text}".'
        + ' Return to <a href="/table">table</a>.'
    )
    if message:
        return exist_msg
    return not_exist_msg


@app.route("/table/<int:message_id>/edit")
def edit_message(message_id):
    message = Message.query.get(message_id)
    not_exist_msg = (
        f"Message {message_id} did not exist and could therefore"
        + ' not be edited. Return to <a href="/table">table</a>.'
    )
    if message:
        message.draft = not message.draft
        db.session.commit()
        return (
            f"Message {message_id} has been editted by toggling draft status."
            + ' Return to <a href="/table">table</a>.'
        )
    return not_exist_msg


@app.route("/table/<int:message_id>/delete", methods=["POST"])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return (
            f"Message {message_id} has been deleted. Return to"
            + ' <a href="/table">table</a>.'
        )
    return (
        f"Message {message_id} did not exist and could therefore not be"
        + ' deleted. Return to <a href="/table">table</a>.'
    )


@app.route("/table/<int:message_id>/like")
def like_message(message_id):
    return (
        f"Liked the message {message_id}. Return to "
        + '<a href="/table">table</a>.'
    )


@app.route("/table/new-message")
def new_message():
    return (
        'Here is the new message page. Return to <a href="/table">table</a>.'
    )


class Msg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


@app.route("/testtable")
def test():
    db.drop_all()
    db.create_all()
    for i in range(10):
        m = Msg(text=f"Test message {i+1}")
        db.session.add(m)
    db.session.commit()
    page = request.args.get("page", 1, type=int)
    pagination = Msg.query.paginate(page, per_page=10)
    messages = pagination.items
    titles = [("id", "#"), ("text", "Message")]
    return render_template("testtable.html", titles=titles, messages=messages)


@app.route("/icon")
def test_icon():
    return render_template("icon.html")


class ChauForm(FlaskForm):
    name = StringField("Name")
    username = StringField(
        "Username", validators=[DataRequired(), Length(1, 20)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(8, 150)]
    )
    remember = BooleanField("Remember me")
    hidden = HiddenField()
    submit = SubmitField()


@app.route("/render_kw_class")
def test_render_kw_class():
    form = ChauForm()
    form.name.render_kw = {"class": "render_kw_class"}
    form.username.render_kw = {"class": "render_kw_class"}
    form.password.render_kw = {"class": "render_kw_class"}
    return render_template_string(
        """
            {% from 'semantic/form.html' import form_field %}
            {% extends 'base.html' %}
            {% block content %}
            <form class="ui form error">
            {{ form_field(form.name) }}
            {{ form_field(form.username, class_='test') }}
            {{ form_field(form.password, class='test') }}
            </form>
            {% endblock content %}
            """,
        form=form,
    )


if __name__ == "__main__":
    app.run(debug=True)