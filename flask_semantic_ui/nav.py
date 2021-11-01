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


"""Flask-SemanticUI.

An implementation of SemanticUI in Flask.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from hashlib import sha1

import attr
from dominate import tags
from visitor import Visitor

# =============================================================================
# CLASSES
# =============================================================================


@attr.s
class SemanticUIRenderer(Visitor):
    """Renderer navbar with Semantic UI Framework."""

    html5 = attr.ib(default=True)
    _in_dropdown = attr.ib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    id = attr.ib(default=None, validator=attr.validators.instance_of(None))

    def visit_Navbar(self, node):
        """Create a navbar id that is somewhat fixed.

        Do not leak any information about memory contents to the outside

        Parameters
        ----------
        node: ``str``
            A node
        Return
        ------
            A root of navbar.
        """
        node_id = self.id or sha1(str(id(node)).encode()).hexdigest()

        root = tags.nav() if self.html5 else tags.div(role="navigation")
        root["class"] = "ui fluid container"

        div_container = tags.div(_class="ui attached stackable menu")
        cont = root.add(div_container)
        # collapse button
        # title may also have a 'get_url()' method, in which case we render
        # a brand-link <a class="item"><i class="mail icon"></i> Messages </a>
        bar = cont.add(
            tags.div(
                _class="menu",
                id=node_id,
            )
        )
        bar_list = bar.add(tags.a(_class="item"))

        for item in node.items:
            bar_list.add(self.visit(item))

        return root

    def visit_Text(self, node):
        """Create a text field for the navbar.

        Parameters
        ----------
        node: ``str``
            A node.
        Return
        ------
            A <div> item with a text for the navbar.
        """
        if not self._in_dropdown:
            return tags.p(node.text, _class="item")
        return tags.div(node.text, _class="item")

    def visit_Link(self, node):
        """Create a link field for the navbar.

        Parameters
        ----------
        node: ``str``
            A node.
        Return
        ------
            A link item <a> with a text for the navbar.
        """
        item = tags.li()
        item.add(tags.a(node.text, _class="item", href=node.get_url()))

        return item

    def visit_Separator(self, node):
        """Create a separator field for the navbar.

        Parameters
        ----------
        node: ``str``
            A node.
        Return
        ------
            A divider item for the navbar.
        """
        if not self._in_dropdown:
            raise RuntimeError("Cannot render separator outside Subgroup.")
        return tags.li(node.text, role="separator", _class="ui divider")

    def visit_Subgroup(self, node, icon="home icon"):
        """Create a Subgroup field for the navbar.

        Parameters
        ----------
        node: ``str``
            A node.
        icon: ``str``
            An icon for the ite. Default value: ``"home icon"``.
        Return
        ------
            A Subgroup item for the navbar.
        """
        if not self._in_dropdown:
            li = tags.div(_class="ui simple dropdown item")
            a = tags.a(node.title, href="#", _class="item")
            menu_dropdown = tags.div(_class="ui simple dropdown item")
            menu_dropdown.add(a)
            a["data-toggle"] = "dropdown"
            a["role"] = "button"
            a["aria-haspopup"] = "true"
            a["aria-expanded"] = "false"
            a.add(tags.span(_class="caret"))
            if node.active:
                a["class"] = "ui active item"

            li.add(tags.i(_class="dropdown icon"))
            ul = li.add(menu_dropdown.add(a.add(tags.i(_class=icon))))

            self._in_dropdown = True
            for item in node.items:

                ul.add(self.visit(item))
            self._in_dropdown = False

            return li
        else:
            raise RuntimeError("Cannot render nested Subgroups")

    def visit_View(self, node):
        """Create a view menu for the navbar.

        Parameters
        ----------
        node: ``str``
            A node.
        Return
        ------
            A menu for the navbar.
        """
        menu = tags.div(_class="ui attached stackable menu")
        item = tags.a(
            node.text, href=node.get_url(), title=node.text, _class="item"
        )
        menu.add(item)
        if node.active:
            item["class"] = "ui active item"
        return menu

    def visit_footer_View(self, node):
        """Create a footer menu.

        Parameters
        ----------
        node: ``str``
            A node.
        Return
        ------
            A menu for the footer.
        """
        menu = tags.div(_class="ui link list")
        item = tags.a(
            node.text, href=node.get_url(), title=node.text, _class="item"
        )
        item.add(item)
        if node.active:
            item["class"] = "ui active item"
        menu.add(item)
        return menu
