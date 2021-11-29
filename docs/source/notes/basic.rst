Basic Usage
===========

Installation
------------

Create a project folder and a :file:`venv` folder within:

.. tabs::

   .. group-tab:: macOS/Linux

      .. code-block:: text

         $ mkdir myproject
         $ cd myproject
         $ python3 -m venv venv

   .. group-tab:: Windows

      .. code-block:: text

         > mkdir myproject
         > cd myproject
         > py -3 -m venv venv

.. code-block:: bash

    $ pip install Flask-SemanticUI


Initialization
--------------

.. code-block:: python

    from flask_semantic import Semantic
    from flask import Flask

    app = Flask(__name__)

    semantic = Semantic(app)


Resources helpers
-----------------

Flask-SemanticUI provides two helper functions to load Semantic UI resources in the template:
``semantic.load_css()`` and ``semantic.load_js()``.

Call it in your base template, for example:

.. code-block:: jinja

    <head>
    ....
    {{ semantic.load_css() }}
    </head>
    <body>
    ...
    {{ semantic.load_js() }}
    </body>

You can pass ``version`` to pin the Semantic UI 2.4.2 version you want to use.
It defaults to load files from CDN. Set ``SEMANTIC_SERVE_LOCAL`` to ``True`` to use built-in local files.
However, these methods are optional, you can also write ``<href></href>`` and ``<script></script>`` tags
to include Semantic UI resources (from your ``static`` folder or CDN) manually by yourself.

Starter template
----------------

For reasons of flexibility, Flask-SemanticUI doesn't include built-in base templates
(this may change in the future). For now,  you have to create a base template yourself.
Be sure to use an HTML5 doctype and include a viewport meta tag for proper responsive behaviors.
Here's an example base template:

.. code-block:: html

    <!doctype html>
    <html lang="en">
        <head>
            {% block head %}
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            {% block styles %}
                <!-- Semantic-UI CSS -->
                {{ semantic.load_css() }}
            {% endblock %}

            <title>Your page title</title>
            {% endblock %}
        </head>
        <body>
            <!-- Your page content -->
            {% block content %}{% endblock %}

            {% block scripts %}
                <!-- Optional JavaScript -->
                {{ semantic.load_js() }}
            {% endblock %}
        </body>
    </html>

Use this in your templates folder (suggested names are ``base.html`` or ``layout.html`` etc.),
and inherit it in child templates. See `Template Inheritance <http://flask.pocoo.org/docs/1.0/patterns/templateinheritance/>`_ for
more details on inheritance.

.. _macros_list:

Macros
------

+------------------------------+--------------------------------+--------------------------------------------------------------------+
| Macro                        | Templates Path                 | Description                                                        |
+==============================+================================+====================================================================+
| render_ui_field()            | semantic/form_ui.html          | Render a WTForms form field.                                       |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_form()             | semantic/form_ui.html          | Render a WTForms form.                                             |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_form_row()         | semantic/form_ui.html          | Render a row of a grid form.                                       |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_hidden_errors()    | semantic/form_ui.html          | Render error messages for hidden form field.                       |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_pager()            | semantic/pagination.html       | Render a basic Flask-SQLAlchemy pagniantion.                       |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_pagination()       | semantic/pagination.html       | Render a standard Flask-SQLAlchemy pagination.                     |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_nav_item()         | semantic/nav.html              | Render a navigation item.                                          |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_breadcrumb_item()  | semantic/nav.html              | Render a breadcrumb item.                                          |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_static()              | semantic/utils.html            | Render a resource reference code (i.e. ``<link>``, ``<script>``).  |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_messages()         | semantic/utils.html            | Render flashed messages send by ``flash()`` function.              |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_icon()             | semantic/utils.html            | Render a Semantic icon.                                            |
+------------------------------+--------------------------------+--------------------------------------------------------------------+
| render_ui_table()            | semantic/table.html            | Render a table with given data.                                    |
+------------------------------+--------------------------------+--------------------------------------------------------------------+

How to use these macros? It's quite simple, just import them from the
corresponding path and call them like any other macro:

.. code-block:: jinja

    {% from 'semantic/form_ui.html' import render_ui_form %}

    {{ render_ui_form(form) }}

Go to the :doc:`macros` page to see the detailed usage for these macros.

Configurations
--------------

+-----------------------------+---------------+------------------------------------------------------------------------------+
| Configuration Variable      | Default Value | Description                                                                  |
+=============================+===============+==============================================================================+
| SEMANTIC_SERVE_LOCAL        | ``False``     | If set to ``True``, local resources will be used for ``load_*`` methods.     |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_BUTTON_STYLE       | ``'primary'`` | Default form button style, will change to ``primary`` in next major release. |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_BUTTON_SIZE        | ``""``        | Default form button size.                                                    |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_ICON_SIZE          | ``None``      | Default icon size.                                                           |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_ICON_COLOR         | ``None``      | Default icon color, follow the context with ``currentColor`` if not set.     |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_MSG_CATEGORY       | ``None'``     | Default flash message category.                                              |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_TABLE_VIEW_TITLE   | ``'View'``    | Default title for view icon of table actions.                                |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_TABLE_EDIT_TITLE   | ``'Edit'``    | Default title for edit icon of table actions.                                |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_TABLE_DELETE_TITLE | ``'Delete'``  | Default title for delete icon of table actions.                              |
+-----------------------------+---------------+------------------------------------------------------------------------------+
| SEMANTIC_TABLE_NEW_TITLE    | ``'New'``     | Default title for new icon of table actions.                                 |
+-----------------------------+---------------+------------------------------------------------------------------------------+

.. 
    tip:: See :ref:`button_customization` to learn how to customize form buttons.
