import os.path

import urwid

from . import signals
from ..utils import debug_log


class ActionBar(urwid.WidgetWrap):

    def __init__(self):
        urwid.WidgetWrap.__init__(self, None)
        self.clear()
        signals.status_message.connect(self.sig_message)
        signals.status_prompt.connect(self.sig_prompt)
        signals.status_prompt_path.connect(self.sig_path_prompt)
        signals.status_prompt_onekey.connect(self.sig_prompt_onekey)

        self.last_path = ""

        self.prompting = False
        self.onekey = False
        self.pathprompt = False

    def sig_message(self, sender, message, expire=None):
        w = urwid.Text(message)
        self._w = w
        self.prompting = False
        if expire:
            def cb(*args):
                if w == self._w:
                    self.clear()
            signals.call_in.send(seconds=expire, callback=cb)

    def prep_prompt(self, p):
        return p.strip() + ": "

    def sig_prompt(self, sender, prompt, text, callback, args=()):
        signals.focus.send(self, section="footer")
        self._w = urwid.Edit(self.prep_prompt(prompt), text or "")
        self.prompting = (callback, args)

    def sig_path_prompt(self, sender, prompt, callback, args=()):
        signals.focus.send(self, section="footer")
        self._w = pathedit.PathEdit(
            self.prep_prompt(prompt),
            os.path.dirname(self.last_path)
        )
        self.pathprompt = True
        self.prompting = (callback, args)

    def sig_prompt_onekey(self, sender, prompt, keys, callback, args=()):
        """
            Keys are a set of (word, key) tuples. The appropriate key in the
            word is highlighted.
        """
        signals.focus.send(self, section="footer")
        prompt = [prompt, " ("]
        mkup = []
        for i, e in enumerate(keys):
            mkup.extend(common.highlight_key(e[0], e[1]))
            if i < len(keys) - 1:
                mkup.append(",")
        prompt.extend(mkup)
        prompt.append(")? ")
        self.onekey = set(i[1] for i in keys)
        self._w = urwid.Edit(prompt, "")
        self.prompting = (callback, args)

    def selectable(self):
        return True

    def keypress(self, size, k):
        if self.prompting:
            if k == "esc":
                self.prompt_done()
            elif self.onekey:
                if k == "enter":
                    self.prompt_done()
                elif k in self.onekey:
                    self.prompt_execute(k)
            elif k == "enter":
                self.prompt_execute(self._w.get_edit_text())
            else:
                if common.is_keypress(k):
                    self._w.keypress(size, k)
                else:
                    return k

    def clear(self):
        self._w = urwid.Text("")
        self.prompting = False

    def prompt_done(self):
        self.prompting = False
        self.onekey = False
        self.pathprompt = False
        signals.status_message.send(message="")
        signals.focus.send(self, section="body")

    def prompt_execute(self, txt):
        if self.pathprompt:
            self.last_path = txt
        p, args = self.prompting
        self.prompt_done()
        msg = p(txt, *args)
        if msg:
            signals.status_message.send(message=msg, expire=1)


class StatusBar(urwid.WidgetWrap):

    def __init__(self, master, helptext):
        self.master, self.helptext = master, helptext
        self.ab = ActionBar()
        self.ib = urwid.WidgetWrap(urwid.Text(""))
        self._w = urwid.Pile([self.ib, self.ab])
        signals.update_settings.connect(self.sig_update_settings)
        signals.flowlist_change.connect(self.sig_update_settings)
        self.redraw()

    def sig_update_settings(self, sender):
        self.redraw()

    def keypress(self, *args, **kwargs):
        return self.ab.keypress(*args, **kwargs)

    def get_status(self):
        r = []

        r.append("[")
        r.append(("heading_key", "H"))
        r.append("eaders]")
        # if self.master.state.default_body_view.name != "Auto":
        #     r.append("[")
        #     r.append(("heading_key", "M"))
        #     r.append(":%s]" % self.master.state.default_body_view.name)

        opts = []
        # if self.master.anticache:
        #     opts.append("anticache")
        opts.append("anticomp")

        if opts:
            r.append("[%s]" % (":".join(opts)))

        return r

    def redraw(self):
        offset = 0
        t = [
            ('heading', ("[%s/%s]" % (offset, 'something')).ljust(9))
        ]

        t.extend(self.get_status())
        debug_log(repr(t))
        status = urwid.AttrWrap(urwid.Columns([
            urwid.Text(t),
            urwid.Text(
                [
                    self.helptext,
                    "[something else]"
                ],
                align="right"
            ),
        ]), "heading")
        self.ib._w = status

    def update(self, text):
        self.helptext = text
        self.redraw()
        self.master.loop.draw_screen()

    def selectable(self):
        return True