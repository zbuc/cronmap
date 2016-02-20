import urwid

from . import tabs, common


class MenuView(tabs.Tabs):
    highlight_color = "focusfield"

    def __init__(self, tab_offset):
        tabs.Tabs.__init__(self,
                           [
                               (self.tab_request, self.view_request),
                               (self.tab_response, self.view_response),
                               (self.tab_details, self.view_details),
                           ],
                           tab_offset
                           )
        self.show()
        self.last_displayed_body = None

    def empty_tab(self):
        txt = common.format_keyvals(
            [(h + ":", v) for (h, v) in [("one", "two"), ("three", "four")]],
            key="header",
            val="text"
        )
        viewmode = "test"
        msg, body = ("test", [urwid.Text([("error", "[content missing]")])])

        cols = [
            urwid.Text(
                [
                    ("heading", msg),
                ]
            ),
            urwid.Text(
                [
                    " ",
                    ('heading', "["),
                    ('heading_key', "m"),
                    ('heading', (":%s]" % viewmode)),
                ],
                align="right"
            )
        ]
        title = urwid.AttrWrap(urwid.Columns(cols), "heading")

        txt.append(title)
        txt.extend(body)

        walker = urwid.SimpleFocusListWalker(txt)
        return urwid.ListBox(walker)

    def tab_request(self):
        return "Request"

    def view_request(self):
        return self.empty_tab()

    def tab_response(self):
        return "Response"

    def view_response(self):
        return self.empty_tab()

    def tab_details(self):
        return "Detail"

    def view_details(self):
        return self.empty_tab()
