from flask import flash, render_template_string


def test_render_messages(app, client):
    @app.route("/messages")
    def test_messages():
        flash("test message", "danger")
        return render_template_string(
            """
                        {% from 'semantic/utils.html' import render_messages %}
                        {{ render_messages() }}
                        """
        )

    @app.route("/container")
    def test_container():
        flash("test message", "danger")
        return render_template_string(
            """
                        {% from 'semantic/utils.html' import render_messages %}
                        {{ render_messages(container=True) }}
                        """
        )

    @app.route("/dismissible")
    def test_dismissible():
        flash("test message", "danger")
        return render_template_string(
            """
                        {% from 'semantic/utils.html' import render_messages %}
                        {{ render_messages(dismissible=True) }}
                        """
        )

    @app.route("/category")
    def test_category():
        flash("A simple default alert—check it out!")
        for category in [
            "dark",
            "danger",
            "debug",
            "light",
            "critical",
            "error",
            "info",
            "warning",
            "success",
            "secondary",
            "primary",
        ]:
            flash(f"A simple {category} alert—check it out!", category)
        return render_template_string(
            """
                        {% from 'semantic/utils.html' import render_messages %}
                        {{ render_messages(dismissible=True) }}
                        """
        )

    response = client.get("/messages")
    data = response.get_data(as_text=True)
    assert '<div class="ui error message">' in data

    response = client.get("/container")
    data = response.get_data(as_text=True)
    assert '<div id="alert" class="ui text container">' in data

    response = client.get("/dismissible")
    data = response.get_data(as_text=True)
    assert '<i id="close-icon" class="close icon"></i>' in data
    assert '<ul class="list">' not in data
    assert "test message" in data

    response = client.get("/category")
    data = response.get_data(as_text=True)
    for cat in ["floating", "black", "error"]:
        assert f'<div class="ui {cat} message">' in data
    # assert 'alert-dismissible' in data
    # assert '<button type="button" class="close" data-dismiss="alert"' in data
    # assert 'fade show' in data
