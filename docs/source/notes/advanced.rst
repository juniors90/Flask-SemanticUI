Advanced Usage
===============

.. _button_customization:

Form Button Customization
--------------------------

Button Style
~~~~~~~~~~~~

When you use form related macros, you have a couple ways to style buttons. Before we start to dive into the solutions, let's
review some Semantic basics: In Semantic, you have 9 normal button style and 8 outline button style, so you have 17 button
style classes below:

- primary
- secondary
- success
- danger
- warning
- info
- light
- dark
- link
- primary
- secondary
- success
- danger
- warning
- info
- light
- dark

Remove the ``ui`` prefix, you will get what we (actually, I) called "Semantic button style name":

- primary
- secondary
- success
- danger
- warning
- info
- light
- dark
- link
- primary
- secondary
- success
- danger
- warning
- info
- light
- dark

You will use these names in Flask-SemanticUI. First, you configuration variables ``SEMANTIC_BUTTON_STYLE`` to set a global form button style:

.. code-block:: python

    from flask import Flask
    from flask_semantic import SemanticUI

    app = Flask(__name__)
    semantic = SemanticUI(app)

    app.config['SEMANTIC_BUTTON_STYLE'] = 'primary'  # default to 'secondary'


Or you can use ``button_style`` parameter when using ``render_ui_form``, ``render_ui_field`` and ``render_ui_form_row``, this parameter will overwrite
``SEMANTIC_BUTTON_STYLE``:

.. code-block:: jinja

    {% from 'semantic/form.html' import render_ui_form %}

    {{ render_ui_form(form, button_style='success') }}

Similarly, you can use this way to control the button size. In Semantic, buttons can have 4 sizes:

- sm
- md (the default size)
- lg
- block

So, the size names used in Flask-SemanticUI will be:

- sm
- md (the default size)
- lg
- block

Now you can use a configuration variable called ``SEMANTIC_BUTTON_STYLE`` to set global form button size:

.. code-block:: python

    from flask import Flask
    from flask_semantic import Semantic

    app = Flask(__name__)
    semantic = Semantic(app)

    app.config['SEMANTIC_BUTTON_SIZE'] = 'sm'  # default to 'md'

there also a parameter called ``button_size`` in form related macros (it will overwrite ``SEMANTIC_BUTTON_SIZE``):

.. code-block:: jinja

    {% from 'semantic/form.html' import render_ui_form %}

    {{ render_ui_form(form, button_size='lg') }}

if you need a **block level small** button (``btn sm block``), you can just do something hacky like this:

.. code-block:: python

    app.config['SEMANTIC_BUTTON_SIZE'] = 'sm block'

What if I have three buttons in one form, and I want they have different styles and sizes? The answer is ``button_map`` parameter in form related macros.
``button_map`` is a dictionary that mapping button field name to Semantic button style names. For example, ``{'submit': 'success'}``.
Here is a more complicate example:

.. code-block:: jinja

    {% from 'semantic/form.html' import render_ui_form %}

    {{ render_ui_form(form, button_map={'submit': 'success', 'cancel': 'secondary', 'delete': 'danger'}) }}

It will overwrite ``button_style`` and ``SEMANTIC_BUTTON_STYLE``.
