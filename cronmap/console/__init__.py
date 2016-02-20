from __future__ import absolute_import

import traceback
import sys

import urwid

from .. import Cronmap
from . import palettes
from .menuview import MenuView


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

    def ticker(self, *userdata):
        #changed = self.tick(self.masterq, timeout=0)
        changed = True
        if changed:
            self.loop.draw_screen()
            # signals.update_settings.send()
        self.loop.set_alarm_in(0.01, self.ticker)

    def shutdown(self):
        pass

    def view_menu(self):
        if self.ui.started:
            self.ui.clear()

        body = MenuView()

        signals.push_view_state.send(
            self,
            window=window.Window(
                self,
                body,
                None,
                statusbar.StatusBar(self, footer),
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
