import urwid

from . import tabs, common, window, signals, nettools, statusbar


class MenuView(tabs.Tabs):
    highlight_color = "focusfield"

    def __init__(self, tab_offset):
        tabs.Tabs.__init__(self,
                           [
                               (self.tab_menu, self.menu_tab),
                               (self.tab_running_jobs, window.empty_tab),
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

    def menu_tab(self):
        body = self.menu_content()
        txt = window.empty_tab(body)

        return txt

    def keypress(self, size, k):
        k = super(self.__class__, self).keypress(size, k)
        if k == "1":
            self.view_network_tools()
        else:
            return k

    def tab_menu(self):
        return "Menu"

    def tab_running_jobs(self):
        return "Running Jobs"

    def view_network_tools(self):
        signals.push_view_state.send(
            self,
            window=window.Window(
                self,
                nettools.NetToolsView(),
                None,
                statusbar.StatusBar(self, nettools.footer),
                None
            )
        )
