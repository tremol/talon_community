from talon.voice import Key, press, Str, Context
from talon import applescript
from ..utils import is_vim


ctx = Context("vim", func=is_vim)


def quit_oni(m):
    applescript.run("""
tell application "Oni"
    quit
end tell
    """)


ctx.keymap({
	"(venom total quit | venom quit yes really | exit application oni)": quit_oni,
	"(vim | venom) save quit": Key(": w q enter"),
	"(vim save | sage)": Key(": w enter"),
	"vim quit": Key(": q enter"), # implemented in window_control
	"(vim | venom) force quit": Key(": q !"), #  | vim quit bang
	"(vim | venom) help": [Key('escape'), ":help "],
	"marco": Key('/'),
	"dizzle": Key('u'),
	"rizzle": Key('ctrl-r'),
	"(trough | window)": Key('ctrl-w'),
	"spark": Key('cmd-v'),

	# vundle
	"plugin install": ":PluginInstall",
	"plugin update": ":PluginUpdate",

	# commentary.vim
	"trundle": Key('g c c'),
	"comment": Key('g c'),

	# vim-unimpaired.vim
	"toggle wrap on": "[ow",
	"toggle wrap off": "]ow",
	"toggle numbers on": "[on",
	"toggle numbers off": "]on",
	"switchee": "[e",
	"switcho": "]e",

	# buffers
	"buffer previous": "[b",	# vim-unimpaired.vim
	"buffer next": "]b",	# vim-unimpaired.vim

})
