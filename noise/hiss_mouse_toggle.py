import time

from talon import ctrl
from talon.audio import noise
from talon_plugins import eye_mouse
from . import pop_sleeping_mouse as sleeping_mouse

# A hiss of one second or longer toggles eye tracking on and off.
# 
# If sleeping mouse is enabled (see pop_sleeping_mouse.py), it will be disabled
# with the first hiss and restored with the second. Note: If sleeping mouse is
# enabled and eye tracking is currently active, the first hiss will only
# disable sleeping mouse and leave the eye tracking active. A second hiss

# Edits may be necessary to play nice with zoom mouse.

class NoiseModel:
    
    def __init__(self):
        self.hiss_start = 0
        self.hiss_last = 0
        self.sleeping_mouse_suspended = False

        noise.register('noise', self.on_noise)

    def on_noise(self, noise):
        now = time.time()
        if noise == 'hiss_start':
            self.hiss_start = now
        elif noise == 'hiss_end':
            duration = time.time() - self.hiss_start
            if duration > 1:
                if eye_mouse.config.control_mouse:
                    if sleeping_mouse.config.enabled:
                        sleeping_mouse.toggle_enabled()
                        self.sleeping_mouse_suspended = True
                    else:
                        eye_mouse.control_mouse.toggle()
                        if self.sleeping_mouse_suspended:
                            sleeping_mouse.toggle_enabled()
                else:
                    if sleeping_mouse.config.enabled:
                        sleeping_mouse.toggle_enabled()
                        self.sleeping_mouse_suspended = True
                    else:
                        self.sleeping_mouse_suspended = False
                    eye_mouse.control_mouse.toggle()

            self.hiss_start = 0

# model = NoiseModel()
