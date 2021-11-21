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

from flask import render_template_string


def test_form_field(app, client, hello_form):
    @app.route("/field")
    def test():
        form = hello_form()
        return render_template_string(
            """
        {% from 'semantic/form.html' import form_field %}
        {{ form_field(form.csrf_token) }}
        {{ form_field(form.hidden) }}
        {{ form_field(form.username) }}
        {{ form_field(form.password) }}
        """,
            form=form,
        )

    response = client.get("/field")
    data = response.get_data(as_text=True)
    # assert '<label for="csrf_token">CSRF Token</label>' not in data
    # assert '<label for="hidden">Hidden</label>' not in data
    assert '<input id="username"' in data
    assert '<input id="password"' in data


def test_form_field_with_render_kw_classes(app, client, hello_form):
    @app.route("/render_kw_class")
    def test_render_kw_class():
        form = hello_form()
        form.name.render_kw = {"class": "render_kw_class"}
        form.username.render_kw = {"class": "render_kw_class"}
        form.password.render_kw = {"class": "render_kw_class"}
        return render_template_string(
            """
            {% from 'semantic/form.html' import form_field %}
            {{ form_field(form.name) }}
            {{ form_field(form.username, class_='test') }}
            {{ form_field(form.password, class='test') }}
            """,
            form=form,
        )

    response = client.get("/render_kw_class")
    data = response.get_data(as_text=True)
    assert '<input class="render_kw_class" id="name" name="name"' in data
    # assert '<input class="test" id="username"' in data
    assert '<input class="test" id="password"' in data


def test_form_field_with_kwargs(app, client, hello_form):
    @app.route("/kwargs_class")
    def test_kwargs_class():
        form = hello_form()
        return render_template_string(
            """
        {% from 'semantic/form.html' import form_field %}
        {{ form_field(form.username, class_='test') }}
        {{ form_field(form.password, class='test') }}
        """,
            form=form,
        )

    response = client.get("/kwargs_class")
    data = response.get_data(as_text=True)
    assert '<input class="test" id="username"' in data
    assert '<input class="test" id="password"' in data

    @app.route("/general_kwargs")
    def test_general_kwargs():
        form = hello_form()
        return render_template_string(
            """
        {% from 'semantic/form.html' import form_field %}
        {{ form_field(form.username, placeholder='test') }}
        {{ form_field(form.password, placeholder='test') }}
        {{ form_field(form.remember, class='test', value='n') }}
        {{ form_field(form.submit, value='test') }}
        """,
            form=form,
        )

    response = client.get("/general_kwargs")
    data = response.get_data(as_text=True)
    assert 'name="username" placeholder="test"' in data
    assert 'name="password" placeholder="test"' in data
    assert (
        '<input class="ui submit button default" id="submit" name="submit"'
        in data
    )
    assert (
        '<input class="ui submit button" id="submit" name="submit"'
        not in data
    )
