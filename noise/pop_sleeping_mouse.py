import time

from talon import ctrl
from talon.audio import noise
from talon_plugins import eye_mouse
from talon_plugins import eye_zoom_mouse

# With this enabled, the first pop will turn the eye mouse on,
# and the second pop will click. The second pop can be replaced with
# several pops in quick succession to double-click, triple-click, etc.

# Note pop.py should also be edited to not conflict with this mouse mode:
# The basic click in that file should be disabled when sleeping mouse is enabled.

# Sleeping mouse settings. Enabled by default.
class config:
    enabled = True
    double_click = 0.25

def toggle_enabled():
    config.enabled = not config.enabled

class NoiseModel:

    def __init__(self):
        self.button = 0
        self.last_click = 0

        noise.register("noise", self.on_noise)

    def on_noise(self, noise):
        if config.enabled and noise == 'pop':
            now = time.time()
            if noise == 'pop' and eye_zoom_mouse.zoom_mouse.enabled:
                return
            elif noise == 'pop' and config.enabled:
                if now - self.last_click < config.double_click:
                    ctrl.mouse_click(button=0, hold=16000)
                    self.last_click = now
                elif eye_mouse.config.control_mouse:
                    ctrl.mouse_click(button=0, hold=16000)
                    self.last_click = now
                    eye_mouse.control_mouse.toggle()
                else:
                    eye_mouse.control_mouse.toggle()
                return
            elif noise == 'pop':
                ctrl.mouse_click(button=0, hold=16000)

model = NoiseModel()

########### 
# The following voice command might better belong in misc/eye_control.py, 
# but is included here to be more self-contained.
###########

from talon.voice import Context

ctx = Context("sleeping_mouse")
ctx.keymap(
    {
        'toggle sleeping mouse':   lambda m: toggle_enabled(),
    }
)
