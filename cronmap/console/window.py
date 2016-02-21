import sys

import urwid

from . import signals, common

from ..utils import debug_log


def common_header():
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


def empty_tab(body=None):
    txt = common_header()

    if body:
        txt.extend(body)

    walker = urwid.SimpleFocusListWalker(txt)
    return urwid.ListBox(walker)


class Window(urwid.Frame):
    def __init__(self, master, body, header, footer, helpctx):
        urwid.Frame.__init__(
            self,
            urwid.AttrWrap(body, "background"),
            header=urwid.AttrWrap(header, "background") if header else None,
            footer=urwid.AttrWrap(footer, "background") if footer else None
        )
        self.master = master
        self.helpctx = helpctx
        signals.focus.connect(self.sig_focus)

    def sig_focus(self, sender, section):
        self.focus_position = section

    def mouse_event(self, *args, **kwargs):
        # args: (size, event, button, col, row)

        k = super(self.__class__, self).mouse_event(*args, **kwargs)
        if not k:
            if args[1] == "mouse drag":
                signals.status_message.send(
                    message="Hold down shift, alt or ctrl to select text.",
                    expire=1
                )
            elif args[1] == "mouse press" and args[2] == 4:
                self.keypress(args[0], "up")
            elif args[1] == "mouse press" and args[2] == 5:
                self.keypress(args[0], "down")
            else:
                return False
            return True

    def keypress(self, size, k):
        debug_log("KP")
        k = super(self.__class__, self).keypress(size, k)
        if k == "?":
            self.master.view_help(self.helpctx)
        elif k == "o":
            self.master.view_options()
        elif k == "Q":
            raise urwid.ExitMainLoop
        elif k == "q":
            signals.pop_view_state.send(self)
        else:
            return k
