from talon.voice import Key, press, Str, Context
from ..utils import is_vim


ctx = Context("vim", func=is_vim)

ctx.keymap({
	"vim save quit": Key("esc : w q enter"),
	"(vim save | sage)": Key("esc : w enter"),
	"vim quit": Key("esc : q"),
	"vim quit bang": Key("esc : q !"),
	"marco": Key('/'),

	# buffers
	
})
