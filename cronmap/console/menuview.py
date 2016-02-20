import urwid

from . import tabs, common


class MenuView(tabs.Tabs):
    highlight_color = "focusfield"

    def __init__(self, tab_offset):
        tabs.Tabs.__init__(self,
                           [
                               (self.tab_menu, self.menu_tab),
                               (self.tab_running_jobs, self.empty_tab),
                           ],
                           tab_offset
                           )
        self.show()
        self.last_displayed_body = None

    def menu_content(self):
        text = []
        text.append(urwid.Text([("head", "\n\ncronmap operations:\n")]))
        menu_options = [
            ("1", "network recon tools"),
            ("2", "osint recon tools"),
            ("3", "view data"),
            ("q", "quit"),
        ]
        text.extend(
            common.format_keyvals(
                menu_options,
                key="key",
                val="text",
                indent=4))

        return text

    def common_header(self):
        txt = common.format_keyvals(
            [(h + ":", v) for (h, v) in
                [("Active Project", "#OpDP"),
                 ("Created", "02-15-2016 00:00:00")]],
            key="header",
            val="text"
        )

        cols = [
            urwid.Text(
                [
                    ("heading", ""),
                ]
            )
        ]
        title = urwid.AttrWrap(urwid.Columns(cols), "heading")

        txt.append(title)

        return txt

    def empty_tab(self, body=None):
        txt = self.common_header()

        if body:
            txt.extend(body)

        walker = urwid.SimpleFocusListWalker(txt)
        return urwid.ListBox(walker)

    def menu_tab(self):
        body = self.menu_content()
        txt = self.empty_tab(body)

        return txt

    def tab_menu(self):
        return "Menu"

    def tab_running_jobs(self):
        return "Running Jobs"
