from talon import ctrl, app
from talon.audio import noise
from ..misc import mouse
from ..misc import switcher

class config:
    enabled = False
    default_scroll_rate = 20
    multiplier = 3
    scroll_rate = 20

def toggle_enabled(m):
    config.enabled = not config.enabled
    ctx2.reload() # enable/disable the settings context
    if config.enabled:
        app.notify("Hiss to Scroll", "Enabled")
    else:
        app.notify("Hiss to Scroll", "Disabled")


def reverse(m):
    config.scroll_rate *= -1

def adjust_speed(multiplier):
    def _adjust_speed(m):
        config.scroll_rate *= multiplier

    return _adjust_speed

def set_speed(multiplier):
    def  _set_speed(m):
        config.scroll_rate = config.default_scroll_rate * multiplier

    return _set_speed

class NoiseModel:
    
    def __init__(self):
        noise.register('noise', self.on_noise)

    def on_noise(self, noise):
        if noise == 'hiss_start':
            if config.enabled:
                mouse.stopScrolling(None)
                mouse.mouse_scroll(config.scroll_rate)(None)
                mouse.startScrolling(None)
        elif noise == 'hiss_end':
            if config.enabled:
                mouse.stopScrolling(None)


model = NoiseModel()

########### 
# The following voice commands might better belong in misc/mouse.py, but are
# included here to be more self-contained.
###########

from talon.voice import Context

ctx1 = Context("hiss_to_scroll")
ctx1.keymap(
    {
        '(toggle hiss | hissy)': [toggle_enabled, set_speed(1)],
        '(toggle hiss | hissy) slower': [toggle_enabled, set_speed(1/config.multiplier)],
        '(toggle hiss | hissy) faster': [toggle_enabled, set_speed(config.multiplier)],
    }
)

ctx2 = Context("hiss_to_scroll_settings", func=lambda app, window: config.enabled)
ctx2.keymap(
    {
        'reverse': reverse,
        'slower': adjust_speed(1/config.multiplier),
        'faster': adjust_speed(config.multiplier),
    }
)
