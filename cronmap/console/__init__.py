from __future__ import absolute_import

import traceback
import sys

import urwid

from .. import Cronmap
from ..utils import debug_log
from . import palettes, signals, window, statusbar, help
from .menuview import MenuView


def _mkhelp():
    text = []
    keys = [
        ("enter/space", "activate option"),
        ("C", "clear all options"),
    ]
    text.extend(common.format_keyvals(keys, key="key", val="text", indent=4))
    return text
help_context = _mkhelp()


class Options(object):
    attributes = [
        "no_mouse",
        "debug",
        "console",
        "palette",
        "palette_transparent",
    ]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        for i in self.attributes:
            if not hasattr(self, i):
                setattr(self, i, None)


class ConsoleMap(Cronmap):
    palette = []

    def __init__(self, options):
        Cronmap.__init__(self, options)

        self.options.console = True
        self.palette = options.palette
        self.palette_transparent = options.palette_transparent

        self.view_stack = []

        signals.call_in.connect(self.sig_call_in)
        signals.pop_view_state.connect(self.sig_pop_view_state)
        signals.push_view_state.connect(self.sig_push_view_state)
        signals.sig_add_event.connect(self.sig_add_event)

    def sig_add_event(self, sender, e, level):
        needed = dict(error=0, info=1, debug=2).get(level, 1)
        if self.options.verbosity < needed:
            return

        if level == "error":
            e = urwid.Text(("error", str(e)))
        else:
            e = urwid.Text(str(e))
        self.eventlist.append(e)
        if len(self.eventlist) > EVENTLOG_SIZE:
            self.eventlist.pop(0)
        self.eventlist.set_focus(len(self.eventlist) - 1)

    def sig_call_in(self, sender, seconds, callback, args=()):
        def cb(*_):
            return callback(*args)
        self.loop.set_alarm_in(seconds, cb)

    def sig_pop_view_state(self, sender):
        if len(self.view_stack) > 1:
            self.view_stack.pop()
            self.loop.widget = self.view_stack[-1]
            debug_log("self.loop.widget: " + repr(self.loop.widget))
        else:
            signals.status_prompt_onekey.send(
                self,
                prompt="Quit",
                keys=(
                    ("yes", "y"),
                    ("no", "n"),
                ),
                callback = self.quit,
            )

    def sig_push_view_state(self, sender, window):
        self.view_stack.append(window)
        self.loop.widget = window
        debug_log("self.loop.widget: " + repr(self.loop.widget))
        debug_log("topmost: " + repr(self.loop._topmost_widget))
        self.loop.draw_screen()

    def ticker(self, *userdata):
        debug_log("ticker")
        changed = False
        if changed:
            self.loop.draw_screen()
            # signals.update_settings.send()
        self.loop.set_alarm_in(0.01, self.ticker)

    def shutdown(self):
        pass

    def view_menu(self):
        tab_offset = 0
        if self.ui.started:
            self.ui.clear()

        body = MenuView(tab_offset)

        debug_log(repr(help_context))
        signals.push_view_state.send(
            self,
            window=window.Window(
                self,
                body,
                None,
                statusbar.StatusBar(self, help.footer),
                help_context
            )
        )

    def run(self):
        self.ui = urwid.raw_display.Screen()
        self.ui.set_terminal_properties(256)
        self.set_palette(self.palette)
        self.loop = urwid.MainLoop(
            urwid.SolidFill("x"),
            screen=self.ui,
            handle_mouse=not self.options.no_mouse,
        )

        self.loop.set_alarm_in(0.01, self.ticker)

        # def exit(s, f):
        #     raise urwid.ExitMainLoop
        # signal.signal(signal.SIGINT, exit)

        self.loop.set_alarm_in(
            0.0001,
            lambda *args: self.view_menu()
        )

        try:
            self.loop.run()
        except Exception:
            self.loop.stop()
            sys.stdout.flush()
            print >> sys.stderr, traceback.format_exc()
            print >> sys.stderr, "cronmap has crashed!"
            print >> sys.stderr, "Please lodge a bug report at:"
            print >> sys.stderr, "\thttps://github.com/zbuc/cronmap"
            print >> sys.stderr, "Shutting down..."
        sys.stderr.flush()
        self.shutdown()


        # while True:
        #     try:
        #         if self.debug:
        #             print "Running scan", datetime.datetime.now()
        #         nmap_out = self._run_scan()

        #         if self.outfile != sys.stdout:
        #             if self.debug:
        #                 print nmap_out

        #         self.outfile.write(nmap_out)
        #         self.outfile.flush()
        #         time.sleep(self.delay)
        #     except KeyboardInterrupt:
        #         if self.outfile is not sys.stdout:
        #             self.outfile.close()
        #         return

    def set_palette(self, name):
        self.palette = name
        self.ui.register_palette(
            palettes.palettes[name].palette(self.palette_transparent)
        )
        self.ui.clear()

    # def view_palette_picker(self):
    #     signals.push_view_state.send(
    #         self,
    #         window = window.Window(
    #             self,
    #             palettepicker.PalettePicker(self),
    #             None,
    #             statusbar.StatusBar(self, palettepicker.footer),
    #             palettepicker.help_context,
    #         )
    #     )
