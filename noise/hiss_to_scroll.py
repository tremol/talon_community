from talon import ctrl, app
from talon.audio import noise
from ..misc import continuous_scroll
from ..utils import is_vim

class config:
    enabled = False
    last_enabled_setting = False
    default_scroll_rate = 13
    multiplier = 3
    scroll_rate = default_scroll_rate 

def toggle_enabled(setting="toggle"):
    def _toggle_enabled(m):
        config.last_enabled_setting = config.enabled
        if setting == "toggle":
            config.enabled = not config.enabled
        elif setting == "on":
            config.enabled = True
        elif setting == "off":
            config.enabled = False
        elif setting == "last":
            config.enabled = config.last_enabled_setting

        ctx2.reload() # enable/disable the settings context
        if config.enabled != config.last_enabled_setting:
            if config.enabled:
                app.notify("Hiss to Scroll", "Enabled")
            else:
                app.notify("Hiss to Scroll", "Disabled")

    return _toggle_enabled

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
        print("noise")
        if noise == 'hiss_start':
            if config.enabled:
                continuous_scroll.stopScrolling(None)
                continuous_scroll.startScrolling(config.scroll_rate)(None)
        elif noise == 'hiss_end':
            if config.enabled:
                continuous_scroll.stopScrolling(None)


model = NoiseModel()

# Disable automatically when certain apps come into focus. Code borrowed from menu.py

from talon import ui

def auto_toggle(app, win):
    if is_vim(app, win):
        toggle_enabled("off")(None)

def ui_event(event, arg):
    if event in ("app_activate", "app_launch", "app_close", "win_open", "win_close"):
        global last_app
        global last_win
        current_app = ui.active_app()
        current_win = ui.active_window()
        # Make sure the window has changed: prevents random toggles when using affected apps
        if (last_app, last_win) != (current_app, current_win):
            (last_app, last_win) = (current_app, current_win)
            auto_toggle(current_app, current_win)

last_app = ui.active_app()
last_win = ui.active_window()

ui.register("", ui_event)


########### 
# The following voice commands might better belong in misc/mouse.py, but are
# included here to be more self-contained.
###########

from talon.voice import Context, Key

ctx1 = Context("hiss_to_scroll")
ctx1.keymap(
    {
        '(toggle hiss | hissy)': [toggle_enabled(), set_speed(1)],
        '(toggle hiss | hissy) on': [toggle_enabled("on"), set_speed(1)],
        '(toggle hiss | hissy) off': [toggle_enabled("off"), set_speed(1)],

        '(toggle hiss | hissy) slower': [toggle_enabled(), set_speed(1/config.multiplier)],
        '(toggle hiss | hissy) faster': [toggle_enabled(), set_speed(config.multiplier)],

        'viper': [toggle_enabled(), set_speed(1), Key("cmd-tab")],
        'viper on': [toggle_enabled("on"), set_speed(1), Key("cmd-tab")],
        'viper off': [toggle_enabled("off"), set_speed(1), Key("cmd-tab")],
    }
)

ctx2 = Context("hiss_to_scroll_settings", func=lambda app, window: config.enabled)
ctx2.keymap(
    {
        'reverse': reverse,
        'slower': adjust_speed(1/config.multiplier),
        'faster': adjust_speed(config.multiplier),
        'default': set_speed(1),
    }
)
