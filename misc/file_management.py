from talon.voice import Context, Key, press
from talon import clip, applescript, resource
from .. import utils
from time import sleep
import subprocess
import json
from fileinput import FileInput
from os import system

def context(app, win):
    if app.bundle == "com.apple.finder":
        return True

ctx = Context("file_management", func=context)

def copy_path_to_clipboard(m):
    x = applescript.run(
        """
    tell application "Finder"
        set sel to the selection as text
        set the clipboard to POSIX path of sel
    end tell
    """
    )

folders = {}
folders_filename = utils.local_filename(__file__, "named_folders.json")
folders.update(json.load(resource.open(folders_filename)))
    
def add_named_folder(m):
    x = copy_path_to_clipboard(None)
    path = clip.get()
    # Stop if it isn't a folder
    if path[-1] != '/':
        return
    filename = path.split('/')[-2]
    keyword = filename.split(' ')[0]

    with FileInput(files=[folders_filename], inplace=True) as f:
        for line in f:
            line = line.rstrip()
            if line in '{}' or line[-1] is ',':
                print(line)
            else:
                print(line + ',')
                print('    "' + keyword + '": "' + path + '"')

# folders = {
#     "computer": "/Users/priggins/_Root/Computer/",
#     "personal": "/Users/priggins/_Root/Personal and Family/",
#     "hobby": "/Users/priggins/_Root/Hobby and Fun/",
#     "work": "/Users/priggins/_Root/Work and Career/",
#     "archival": "/Users/priggins/_Root/Archival/",
#     "backups": "/Users/priggins/_Root/Backups/",
# }

def move_files_to_named_folder(m):
    x = copy_path_to_clipboard(None)
    origin_files = clip.get()
    # Split multiple files into a list.
    #   This will break if any file paths include Macintosh HD!
    origin_files = origin_files.split("Macintosh HD")
    # Return if any of the file paths don't start with /
    #   This might happen if any file paths include Macintosh HD
    if not all([f[0] is "/" for f in origin_files]):
        return
    keyword = m['file_management.folders']
    path = str(folders[keyword[0]])
    subprocess.run(["/bin/mv", "-n"] + origin_files + [path])

def go_to_named_folder(m):
    keyword = m['file_management.folders']
    path = str(folders[keyword[0]])
    press('cmd-shift-g')
    # sleep(0.3)
    utils.insert(path)
    press('enter')
 
def link_to_named_folder(m):
    x = copy_path_to_clipboard(None)
    origin_file = clip.get()
    if "Macintosh HD" in origin_file:
        return
    keyword = m['file_management.folders']
    path = str(folders[keyword[0]])
    subprocess.run(["/bin/ln", "-s", origin_file, path])

ctx.keymap({
    "copy path to clipboard": copy_path_to_clipboard, 
    "add this folder": add_named_folder,
    "edit named folders": lambda m: system("open -a 'MacVim' " + folders_filename),
    "(move this to | put in) {file_management.folders}": move_files_to_named_folder,
    # "undo last move": undo_last_move, # NOT YET IMPLEMENTED
    "go to {file_management.folders}": go_to_named_folder,
    "link [this] to {file_management.folders}": link_to_named_folder,
})

ctx.set_list('folders', folders)