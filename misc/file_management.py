from talon.voice import Context, Key
from talon import clip
import subprocess

def context(app, win):
    if app.bundle == "com.apple.finder":
        return True

ctx = Context("file_management", func=context))

def copy_path_to_clipboard(m):
    x = applescript.run(
        """
    tell application "Finder"
        set sel to the selection as text
        set the clipboard to POSIX path of sel
    end tell
    """
    )

folders = {
    
}

def move_file_to_clipboard(m):
    path = clip.get()
    subprocess.run(["/bin/mv",
                    path + "/Users/priggins/_Root/Computer"])

ctx.keymap({
    # file movement commands
    "move to computer": 
})

ctx.set_list('folders', folders)