import time

from talon import ctrl, app, ui
from talon.voice import Context
from talon.audio import noise
from talon.webview import Webview
from ..utils import spoken_text
from . import pop_control as pc

# With this enabled, pops will alternate dictation and non-dictation

# Sleeping mouse settings. Enabled by default.
class config:
    dictation_enabled = False
    greedy = False

def toggle_enabled():
    config.dictation_enabled = not config.dictation_enabled
    update_context_and_webview()

template = """
<style type="text/css">
body {
    width: 200px;
    padding: 0;
    margin: 0;
}
</style>
<h3 id="title">DICTATION ON!</h3>
<br>
<br>
Greedy: {{ greedy }}
<br>
<br>
<br>
"""
webview = Webview()
webview.move(ui.main_screen().width-250, ui.main_screen().height-270)

def update_context_and_webview():
    ctx1.reload()
    ctx2.reload()
    ctx3.reload()

    if config.dictation_enabled:
        webview.render(template, greedy=str(config.greedy))
        webview.show()
    else:
        webview.hide()

def toggle_greedy(TRUEFALSE):
    def _toggle_greedy(m):
        config.greedy = TRUEFALSE
        # app.notify(title="Pop Dictation", body="Greedy: " + str(TRUEFALSE))
        update_context_and_webview()
    return _toggle_greedy

class NoiseModel:

    def __init__(self):
        self.button = 0
        self.last_click = 0

        noise.register("noise", self.on_noise)

    def on_noise(self, noise):
        if pc.PopControl.mode == pc.PopControl.DICTATION and noise == 'pop':
            print("noise: pop")
            toggle_enabled()
            # app.notify(title="dictation: " + str(config.dictation_enabled), body="greedy: " + str(config.greedy))
            update_webview()

model = NoiseModel()

# ctx1 = Context("dictation_greedy", func=lambda app, window:  config.dictation_enabled and config.greedy)
ctx1 = Context("dictation_greedy", func=lambda app, window: pc.PopControl.mode == pc.PopControl.DICTATION and config.dictation_enabled and config.greedy)
ctx1.keymap(
    {
        "<dgndictation>++": [spoken_text, " "]
    }
)

ctx2 = Context("dictation_not_greedy", func=lambda app, window:  config.dictation_enabled and not config.greedy)
# ctx2 = Context("dictation_not_greedy", func=lambda app, window: pc.PopControl.mode == pc.PopControl.DICTATION and config.dictation_enabled and not config.greedy)
ctx2.keymap(
    {
        "<dgndictation>": [spoken_text, " "]
    }
)

ctx3 = Context("dictation_settings")
# ctx3 = Context("dictation_settings", func=lambda app, window: pc.PopControl.mode == pc.PopControl.DICTATION)
ctx3.keymap(
    {
        "greedy on": toggle_greedy(True),
        "greedy off": toggle_greedy(False),
    }
)
