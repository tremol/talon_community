import time

from talon import ctrl
from talon import tap
from talon.audio import noise
from talon.track.geom import Point2d
from talon_plugins import eye_mouse
from talon_plugins import eye_zoom_mouse
from user import sleeping_mouse

class NoiseModel:
    def __init__(self):
        self.hiss_start = 0
        self.hiss_last = 0
        self.button = 0
        self.mouse_origin = Point2d(0, 0)
        self.mouse_last = Point2d(0, 0)
        self.dragging = False
        self.last_click = 0

        tap.register(tap.MMOVE, self.on_move)
        noise.register('noise', self.on_noise)

    def on_move(self, typ, e):
        if typ != tap.MMOVE: return
        self.mouse_last = pos = Point2d(e.x, e.y)
        duration = time.time() - self.hiss_start
        if self.hiss_start and not self.dragging:
            if (pos - self.mouse_origin).len() > 10 and duration > 1:
                self.dragging = True
                self.button = 0
                x, y = self.mouse_origin.x, self.mouse_origin.y
                ctrl.mouse(x, y)
                ctrl.mouse_click(x, y, button=0, down=True)
                ctrl.mouse(pos.x, pos.y)

    def on_noise(self, noise):
        now = time.time()
        if noise == 'pop' and eye_zoom_mouse.zoom_mouse.enabled:
            return
        elif noise == 'pop' and sleeping_mouse.config.enabled:
            if now - self.last_click < sleeping_mouse.config.double_click:
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
        # elif noise == 'hiss_start':
        #     self.mouse_origin = self.mouse_last
        #     self.hiss_start = now
        # elif noise == 'hiss_end':
        #     if self.dragging:
        #         ctrl.mouse_click(button=self.button, up=True)
        #         self.dragging = False
        #     self.hiss_start = 0
        # elif noise == 'hiss_start':
        #     if now - self.hiss_last < 0.25:
        #         ctrl.mouse_click(button=self.button, down=True)
        #         self.hiss_last = now
        #         self.dragging = True
        #     else:
        #         self.mouse_origin = self.mouse_last
        #     self.hiss_start = now
        # elif noise == 'hiss_end':
        #     if self.dragging:
        #         ctrl.mouse_click(button=self.button, up=True)
        #         self.dragging = False
        #     else:
        #         duration = time.time() - self.hiss_start
        #         if duration > 0.5:
        #             self.button = 1
        #             ctrl.mouse_click(button=1)
        #             self.hiss_last = now
        #         elif duration > 0.2:
        #             self.button = 0
        #             ctrl.mouse_click(button=0)
        #             self.hiss_last = now
        #     self.hiss_start = 0

model = NoiseModel()
