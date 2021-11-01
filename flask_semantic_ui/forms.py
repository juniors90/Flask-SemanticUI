#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file was part of Flask-Bootstrap and was modified under the terms of
# its BSD License. Copyright (c) 2013, Marc Brinkmann. All rights reserved.
#
# This file is part of the
# Flask-SemanticUI Project (https://github.com/juniors90/Flask-SemanticUI/).
# Copyright (c) 2022, Ferreira Juan David
# License: MIT
# Full Text: https://github.com/juniors90/Flask-SemanticUI/blob/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================


"""
Flask-SemanticUI.
Implementation of SemanticUI in Flask.
"""

# =============================================================================
# IMPORTS
# =============================================================================


from dominate import tags
from dominate.util import raw
from flask import current_app
from markupsafe import Markup
from visitor import Visitor

# 33-36, 49-54, 57-58, 63-76, 81-85, 88-94, 97, 100, 104,
# 109, 114-123, 126-127, 131, 134-157, 160, 164, 167,
# 170-173, 177, 180-185


def render_form(form, **kwargs):
    r = WTFormsRenderer(**kwargs)
    markup = Markup(r.visit(form))

    return markup


class WTFormsRenderer(Visitor):
    def __init__(
        self,
        action="",
        id=None,
        method="post",
        extra_classes=[],
        role="form",
        enctype=None,
    ):
        self.action = action
        self.form_id = id
        self.method = method
        self.extra_classes = extra_classes
        self.role = role
        self.enctype = enctype

    def _visited_file_field(self):
        if self._real_enctype is None:
            self._real_enctype = "multipart/form-data"

    def _get_wrap(self, node, classes="form-group"):
        # add required class, which strictly speaking isn't bootstrap, but
        # a common enough customization
        if node.flags.required:
            classes += " required"

        div = tags.div(_class=classes)
        if current_app.debug:
            div.add(
                tags.comment(
                    " Field: {} ({}) ".format(
                        node.name, node.__class__.__name__
                    )
                )
            )

        return div

    def _wrapped_input(
        self, node, type="text", classes=["ui control"], **kwargs
    ):
        wrap = self._get_wrap(node)
        wrap.add(tags.label(node.label.text, _for=node.id))
        wrap.add(tags.input(type=type, _class=" ".join(classes), **kwargs))

        return wrap

    def visit_BooleanField(self, node):
        wrap = self._get_wrap(node, classes="checkbox")

        label = wrap.add(tags.label(_for=node.id))
        label.add(tags.input(type="checkbox"))
        label.add(node.label.text)

        return wrap

    def visit_DateField(self, node):
        return self._wrapped_input(node, "date")

    def visit_DateTimeField(self, node):
        return self._wrapped_input(node, "datetime-local")

    def visit_DecimalField(self, node):
        # FIXME: if range-validator is present, add limits?
        return self._wrapped_input(node, "number")

    def visit_EmailField(self, node):
        # note: WTForms does not actually have an EmailField, this function
        # is called by visit_StringField based on which validators are enabled
        return self._wrapped_input(node, "email")

    def visit_Field(self, node):
        # FIXME: add error class

        wrap = self._get_wrap(node)

        # add the label
        wrap.add(tags.label(node.label.text, _for=node.id))
        wrap.add(raw(node()))

        if node.description:
            wrap.add(tags.p(node.description, _class="help-block"))

        return wrap

    def visit_FileField(self, node):
        self._visited_file_field()
        return self._wrapped_input(node, "file", classes=[])

    def visit_FloatField(self, node):
        # FIXME: if range-validator is present, add limits?
        return self._wrapped_input(node, "number")

    def visit_Form(self, node):
        form = tags.form(_class=" ".join(["ui form"] + self.extra_classes))

        if self.action:
            form["action"] = self.action

        if self.form_id:
            form["id"] = self.form_id

        if self.method:
            form["method"] = self.method

        # prepare enctype, this will be auto-updated by file fields if
        # necessary
        self._real_enctype = self.enctype

        # render fields
        for field in node:
            elem = self.visit(field)
            form.add(elem)

        if self._real_enctype:
            form["enctype"] = self._real_enctype

        return form

    def visit_HiddenField(self, node):
        return raw(node())

    def visit_IntegerField(self, node):
        # FIXME: if range-validator is present, add limits?
        return self._wrapped_input(node, "number", step=1)

    def visit_PasswordField(self, node):
        return self._wrapped_input(node, "password")

    def visit_SubmitField(self, node):
        button = tags.button(
            node.label.text, _class="ui submit button", type="submit"
        )
        return button

    def visit_TextField(self, node):
        # legacy support for TextField, deprecated in WTForms 2.0
        return self.visit_StringField(node)

    def visit_StringField(self, node):
        for v in node.validators:
            if v.__class__.__name__ == "Email":
                # render email fields differently
                return self.visit_EmailField(node)

        return self._wrapped_input(node, "text")
