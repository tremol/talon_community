from talon import app, clip, ui
from talon.voice import Context, Str

ctx = Context("talon_helpers")

def copy_bundle(m):
    bundle = ui.active_app().bundle
    clip.set(bundle)
    app.notify('Copied app bundle', body='{}'.format(bundle))


ctx.keymap({
        'copy active bundle': copy_bundle,
        "raw talon phrase <phrase> [over]": lambda m: Str(str(m))(None),
        "raw talon word <word> [over]": lambda m: Str(str(m))(None),
})
