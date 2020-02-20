from talon import app
from talon.voice import Context

class PopControl:
    mode = 2

    DICTATION = 1
    MOUSE = 2

def set_mode(MODE):
    def _set_mode(m):
        PopControl.mode = MODE
        app.notify(title="Pop Mode", body={1:"Dictation", 2:"Mouse"}[MODE])
    return _set_mode

ctx = Context("pop_control")
ctx.keymap(
    {
        'popper venom':   set_mode(PopControl.DICTATION),
        'popper mouse':   set_mode(PopControl.MOUSE),
    }
)
