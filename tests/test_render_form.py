from flask import render_template_string
from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    MultipleFileField,
    PasswordField,
    StringField,
    SubmitField)


def test_render_form(app, client, example_form):
    @app.route("/form")
    def test():
        form = example_form()
        return render_template_string(
            """
                {% import "semantic_ui/wtf.html" as wtf %}
                {{ wtf.quick_form(form,
                                  form_title='Title for Shipping Information',
                                  extra_classes='inverted',
                                  form_type='horizontal',
                                  button_map={'submit_button': 'primary'})}}
                """,
            form=form,
        )

    response = client.get("/form")
    data = response.get_data(as_text=True)
    assert '<input class="ui field" id="name" name="name"' in data
    assert '<input class="ui field" id="username" name="username"' in data
    assert '<input class="ui field" id="country_code"' in data
    assert '<input id="radio_field-0" name="radio_field"' in data
    assert '<input class="ui submit button primary" id="submit_button"' in data


# test WTForm field description for TextFieldField
def test_form_description_for_textfield(app, client):
    class TestForm(FlaskForm):
        field1 = StringField("First Field", description="This is field one.")
        submit_button = SubmitField("Submit Form")

    @app.route("/description")
    def description():
        form = TestForm()
        return render_template_string(
            """
                    {% import "semantic_ui/wtf.html" as wtf %}
                    {{ wtf.quick_form(form,
                                form_title='Title for Shipping Information',
                                button_map={'submit_button': 'primary'}) }}
                    """,
            form=form,
        )

    response = client.get("/description")
    data = response.get_data(as_text=True)
    assert "Title for Shipping Information" in data
    assert "<p>This is field one.</p>" in data
    assert '<input id="field1" name="field1" type="text" value="">' in data


# test WTForm fields for render_form and render_field
def test_render_form_enctype(app, client):
    class SingleUploadForm(FlaskForm):
        sample = FileField("Sample upload")
        submit_button = SubmitField("Submit Form")

    class MultiUploadForm(FlaskForm):
        photos = MultipleFileField("Multiple photos")
        submit_button = SubmitField("Submit Form")

    @app.route("/single")
    def single():
        form = SingleUploadForm()
        return render_template_string(
            """
            {% import "semantic_ui/wtf.html" as wtf %}
            {{ wtf.quick_form(form,
                                form_title='Title for Shipping Information',
                                button_map={'submit_button': 'primary'}) }}
        """,
            form=form,
        )

    @app.route("/multi")
    def multi():
        form = MultiUploadForm()
        return render_template_string(
            """
            {% import "semantic_ui/wtf.html" as wtf %}
            {{ wtf.quick_form(form,
                                form_title='Title for Shipping Information',
                                button_map={'submit_button': 'primary'}) }}
        """,
            form=form,
        )

    response = client.get("/single")
    data = response.get_data(as_text=True)
    assert "multipart/form-data" in data

    response = client.get("/multi")
    data = response.get_data(as_text=True)
    assert "multipart/form-data" in data


# test render_kw class for WTForms field
def test_form_render_kw_class(app, client):
    class LoginForm(FlaskForm):
        username = StringField(
            "Username", render_kw={"class": "my-awesome-class"}
        )
        phone = PasswordField(
            "Password", render_kw={"class": "my-password-class"}
        )
        submit_button = SubmitField(
            "Submit Form", render_kw={"class": "class-not-found"}
        )

    @app.route("/render_kw")
    def render_kw():
        form = LoginForm()
        return render_template_string(
            """
            {% import "semantic_ui/wtf.html" as wtf %}
            {{ wtf.quick_form(form,
                form_title='Title for Shipping Information',
                button_map={'submit_button': 'my-class-customs'}) }}
            """,
            form=form,
        )

    response = client.get("/render_kw")
    data = response.get_data(as_text=True)
    assert 'class="my-password-class"' in data
    assert "class-not-found" not in data
    assert 'class="my-awesome-class"' in data
    assert 'class="ui submit button my-class-customs"' in data
