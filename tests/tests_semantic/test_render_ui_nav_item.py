from flask import render_template_string


def test_render_render_ui_nav_item_active(app, client):
    @app.route("/active")
    def foo():
        return render_template_string(
            """
                {% from 'semantic/nav.html' import render_ui_nav_item %}
                {{ render_ui_nav_item('foo', 'Foo') }}
                """
        )

    response = client.get("/active")
    data = response.get_data(as_text=True)
    assert ' <a class="active item"' in data

    @app.route("/not_active")
    def bar():
        return render_template_string(
            """
                {% from 'semantic/nav.html' import render_ui_nav_item %}
                {{ render_ui_nav_item('foo', 'Foo') }}
                """
        )

    response = client.get("/not_active")
    data = response.get_data(as_text=True)
    assert '<a class="item"' in data

    @app.route("/color")
    def color():
        return render_template_string(
            """
            {% from 'semantic/nav.html' import render_ui_nav_item %}
            {{ render_ui_nav_item('color',
                                  'Color',
                                  icon='envelope',
                                  color='teal') }}
            """
        )

    response = client.get("/color")
    data = response.get_data(as_text=True)
    assert '<a class="active teal item" href="/color">' in data
    assert '<i class="envelope icon"></i>Color</a>' in data
