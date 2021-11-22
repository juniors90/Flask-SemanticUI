from flask import render_template_string


def test_render_breadcrumb_item_active(app, client):
    @app.route("/not_active_item")
    def foo():
        return render_template_string(
            """
            {% from 'semantic/nav.html' import render_breadcrumb_sui_item %}
            {{ render_breadcrumb_sui_item('bar', 'Bar') }}
                """
        )

    @app.route("/active_item")
    def bar():
        return render_template_string(
            """
            {% from 'semantic/nav.html' import render_breadcrumb_sui_item %}
            {{ render_breadcrumb_sui_item('bar', 'Bar') }}
            """
        )

    response = client.get("/not_active_item")
    data = response.get_data(as_text=True)
    assert '<a class="section" href="/active_item">Bar</a>' in data

    response = client.get("/active_item")
    data = response.get_data(as_text=True)
    assert '<a class="active section">Bar</a>' in data
    assert '<i class="right chevron icon divider"></i>' in data
