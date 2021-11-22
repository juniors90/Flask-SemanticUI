from flask import render_template_string


def test_form_field_row(app, client, hello_form):
    @app.route("/form")
    def test():
        form = hello_form()
        return render_template_string(
            """
                {% from 'semantic/form_ui.html' import form_field_row %}
                {{ form_field_row([form.username, form.password]) }}
                """,
            form=form,
        )

    response = client.get("/form")
    data = response.get_data(as_text=True)
    assert '<div class="two fields">' in data
    assert '<div class="field required">' in data
    assert 'input class="" id="username' in data
    assert '<input class="" id="password"' in data
