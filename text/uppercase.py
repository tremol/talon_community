from talon.voice import Context, Key
import string
from ..utils import insert

# upper_alphabet_words = "append backer change delete ender finder gutter high insert join keyword lower middle next open paste command replace sneaker teeter undo visual wordy exit yanker zoink"
upper_alphabet_words = "ash baker chain dog egg fox gig horse ice jake king lash mule net oak page quail raft scout tide use vessel winch xray yacht zoo" 

alphabet_upper = dict(zip(upper_alphabet_words.split(), string.ascii_uppercase))
print(alphabet_upper)

def upper(m):
    s = m['uppercase.alphabet_upper']
    c = str(alphabet_upper[s[0]])
    insert(c)


# ctx = Context("uppercase", bundle="org.vim.MacVim")
ctx = Context("uppercase")

ctx.keymap(
    {
        "{uppercase.alphabet_upper}": upper,
    }
)
ctx.set_list('alphabet_upper', alphabet_upper)
