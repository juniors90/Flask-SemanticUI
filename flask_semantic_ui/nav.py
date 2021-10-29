from hashlib import sha1
from dominate import tags
from visitor import Visitor


class SemanticUIRenderer(Visitor):
    def __init__(self, html5=True, id=None):
        self.html5 = html5
        self._in_dropdown = False
        self.id = id

    def visit_Navbar(self, node):
        # create a navbar id that is somewhat fixed, but do not leak any
        # information about memory contents to the outside
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
        if not self._in_dropdown:
            return tags.p(node.text, _class="item")
        return tags.div(node.text, _class="item")

    def visit_Link(self, node):
        item = tags.li()
        item.add(tags.a(node.text, _class="item", href=node.get_url()))

        return item

    def visit_Separator(self, node):
        if not self._in_dropdown:
            raise RuntimeError("Cannot render separator outside Subgroup.")
        return tags.li(node.text, role="separator", _class="ui divider")

    def visit_Subgroup(self, node, icon="home icon"):
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
        menu = tags.div(_class="ui attached stackable menu")
        item = tags.a(
            node.text, href=node.get_url(), title=node.text, _class="item"
        )
        menu.add(item)
        if node.active:
            item["class"] = "ui active item"

    def visit_footer_View(self, node):
        menu = tags.div(_class="ui link list")
        item = tags.a(
            node.text, href=node.get_url(), title=node.text, _class="item"
        )
        item.add(item)
        if node.active:
            item["class"] = "ui active item"
        menu.add(item)
        return menu
