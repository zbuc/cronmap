# -*- coding: utf-8 -*-
from __future__ import absolute_import

import urwid

from . import common, signals, window, statusbar
from .. import version
from ..utils import debug_log

footer = [
    ("heading", 'cronmap v%s ' % version.VERSION),
    ('heading_key', "q"), ":back ",
]


class NetToolsView(urwid.ListBox):
    def __init__(self, view=None):
        if view and hasattr(self, view):
            urwid.ListBox.__init__(
                self,
                getattr(self, view)()
            )
        else:
            urwid.ListBox.__init__(
                self,
                self.tools_list()
            )

    def tools_list(self):
        text = window.common_header()
        text.append(urwid.Text([("head", "\n\ncronmap operations:\n")]))
        menu_options = [
            ("1", "nmap"),
            ("2", "s̶k̶i̶p̶f̶i̶s̶h̶"),
            ("3", "d̶n̶s̶ i̶n̶f̶o̶  (w̶h̶o̶i̶s̶, d̶i̶g̶)"),
            ("4", "r̶o̶b̶t̶e̶x̶"),
            ("q", "back up"),
        ]
        text.extend(
            common.format_keyvals(
                menu_options,
                key="key",
                val="text",
                indent=4))

        return text

    def nmap_view(self):
        signals.push_view_state.send(
            self,
            window=window.Window(
                self,
                self.__class__("nmap_config"),
                None,
                statusbar.StatusBar(self, footer),
                None
            )
        )

    def nmap_config(self):
        text = window.common_header()
        text.append(urwid.Text([("head", "\n\nnmap configuration:\n")]))
        menu_options = [
            ("hosts", "['192.168.1.1', '127.0.0.1']"),
            ("arguments", "-sV -Pn -p0-65535"),
            ("1", "queue scan"),
            ("q", "back up"),
        ]
        text.extend(
            common.format_keyvals(
                menu_options,
                key="key",
                val="text",
                indent=4))

        return text

    def keypress(self, size, k):
        k = super(self.__class__, self).keypress(size, k)
        if k == "1":
            debug_log("load nmap view")
            self.nmap_view()
        else:
            return k
