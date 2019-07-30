from talon import ctrl
from talon.audio import noise
from . import pop_sleeping_mouse as sleeping_mouse


class NoiseModel:
    def __init__(self):
        self.button = 0

        noise.register("noise", self.on_noise)

    def on_noise(self, noise):
        # don't click here if sleeping mouse is on
        if noise == "pop" and not sleeping_mouse.config.enabled:
            ctrl.mouse_click(button=0, hold=16000)


model = NoiseModel()
