# From https://github.com/talonvoice/examples
from talon_plugins import eye_mouse
from talon.voice import Context
from ..noise.pop_control import PopControl

def control_mouse(m):
    eye_mouse.control_mouse.toggle()
    PopControl.mode = PopControl.MOUSE

ctx = Context("eye_control")
ctx.keymap(
    {
        "debug overlay": lambda m: eye_mouse.debug_overlay.toggle(),
        "control mouse": control_mouse,
        # "control mouse": lambda m: eye_mouse.control_mouse.toggle(),
        "camera overlay": lambda m: eye_mouse.camera_overlay.toggle(),
        "run calibration": lambda m: eye_mouse.calib_start(),
    }
)
