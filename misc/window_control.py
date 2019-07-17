from os import system

from talon.voice import Context, Key, press
from ..utils import parse_words_as_integer, is_vim, is_not_vim

ctx_not_vim = Context("window_control-no_vim", func=is_not_vim)
ctx_vim = Context("window_control-vim", func=is_vim)


def jump_tab(m):
    tab_number = parse_words_as_integer(m._words[1:])
    if tab_number is not None and tab_number > 0 and tab_number < 9:
        press("cmd-%s" % tab_number)

common = {
        # "[switch] space (right | next)": Key("ctrl-right"),
        "desk right": Key("ctrl-right"),
        # "[switch] space (left | previous | preev)": Key("ctrl-left"),
        "desk left": Key("ctrl-left"),
        "(minimise window | curtail)": Key("cmd-m"),
        "show app windows": Key("ctrl-down"),
        # application navigation
        "[open] launcher": Key("cmd-space"),
        "([switch] app (next | right) | swick)": Key("cmd-tab"),
        "[switch] app (left | previous | preev)": Key("cmd-shift-tab"),
        "([open] mission control | mission)": lambda m: system("open -a 'Mission Control'"),
}

ctx_not_vim.keymap(
    {
        **common,
        # tab control
        "(open | new) tab": Key("cmd-t"),
        "(close tab | peachy)": Key("cmd-w"),
        "([switch] tab (right | next) | goneck)": Key("cmd-shift-]"),
        "([switch] tab (left | previous | preev) | gopreev)": Key("cmd-shift-["),
        "[switch] tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "[switch] tab (end | rightmost)": Key("cmd-9"),
        # zooming
        "(zoom in | shompla)": Key("cmd-="),
        "(zoom out | shaman)": Key("cmd--"),
        "zoom normal": Key("cmd-0"),
        # window control
        "(open | new) window": Key("cmd-n"),
        "window close": Key("cmd-shift-w"),
        "([switch] window next | gibby)": Key("cmd-`"),
        "([switch] window (previous | preev) | shibby)": Key("cmd-shift-`"),
    }
)

ctx_vim.keymap(
    {
        **common,
        # tab control
        "(open | new) tab": [Key('escape'), ":tabnew", Key('enter')],
        "(close tab | peachy)": [Key('escape'), ":q", Key('enter')],
        "([switch] tab (right | next) | goneck)": Key("cmd-shift-]"),
        "([switch] tab (left | previous | preev) | gopreev)": Key("cmd-shift-["),
        "[switch] tab (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8)": jump_tab,
        "[switch] tab (end | rightmost)": Key("cmd-9"),
        # zooming
        "(zoom in | shompla)": Key("cmd-="),
        "(zoom out | shaman)": Key("cmd--"),
        "zoom normal": Key("cmd-0"),
        # window control
        "(open | new) window": Key("cmd-n"),
        "window close": Key("cmd-shift-w"),
        "([switch] window next | gibby)": Key("cmd-`"),
        "([switch] window (previous | preev) | shibby)": Key("cmd-shift-`"),
    }
)
