from talon.voice import Key, press, Str, Context
from talon import applescript
from ..utils import is_vim, text


ctx = Context("MacVim", bundle="org.vim.MacVim")

LEADER = "\\"

ctx.keymap({
    # duplicating from generic editor:
    # meta
    "(save it | sage)": Key("cmd-s"),
    "(undo it | dizzle)": Key("cmd-z"),
    "(redo it | rizzle)": Key("cmd-shift-z"),
    # clipboard
    "(clip cut | snatch)": Key("cmd-x"),
    "(clip copy | stoosh)": Key("cmd-c"),
    "(clip paste | spark)": Key("cmd-v"),
    # motions
    "peg": Key("alt-left"),
    "fran": Key("alt-right"),
    "ricky": Key("cmd-right"),
    "lefty": Key("cmd-left"),

    # miscellaneous helpers
    "current directory": LEADER + "Tpwd", # :pwd<CR>
    "working directory": LEADER + "Tcwd", # :echo getcwd()<CR>
    "(vim | venom) grep": LEADER + "Tvim", # :vim // **<Left><Left><Left><Left>
    "source config": LEADER + "Tvrc", # :source $MYVIMRC<CR>
    "sixty one a check": LEADER + "Tcsa", # [[w:lcd %%<CR>:!python3 ok -q <c-r><c-w><CR>

    # for correcting accidental 6G instead of 6j/6k
    "line oops down": LEADER + "Gj",
        # map <leader>Gj :let @g=v:prevcount<CR>'':norm <c-r>gj<CR>zz
    "line oops up": LEADER + "Gk",
        # map <leader>Gk :let @g=v:prevcount<CR>'':norm <c-r>gk<CR>zz

    # tree style notes
    "level one": [Key("escape"), LEADER + "Tnl1"], # o\|-- 
    "new level": [Key("escape"), LEADER + "Tnnl"], # yypf-C-- ... sorta 
    "new sublevel": [Key("escape"), LEADER + "Tnsl"], # yypI\|   <Esc>f-C-- 
    "level up": [Key("escape"), LEADER + "Tnlu"], # I\|   <Esc>A
    "level down": [Key("escape"), LEADER + "Tnld"], # 0dt\|A

    # basics
    "(vim | venom) save quit": LEADER + "Twqq", # :wq<CR>
    "(vim | venom) quit": LEADER + "Tqqq", # :q<CR>
    "(vim | venom) force quit": LEADER + "TqqQ", # :q!<CR>
    "(vim | venom) help [<dgndictation>]": [":help ", text],
    "marco": Key('/'),
    "dizzle": Key('u'),
    "rizzle": Key('ctrl-r'),
    "(trough | window)": Key('ctrl-w'),
    "kite": [Key("alt-right"), Key("ctrl-w")],
    "nudgle": [Key("alt-left"), Key("backspace")],
    "jolt": "yyp",
    "shabble": Key("cmd-["),
        # nmap <D-[> <<
        # vmap <D-[> <gv
    "shabber": Key("cmd-]"),
        # nmap <D-]> >>
        # vmap <D-]> >gv
    "moment": Key("ctrl-o"),


    # aesthetics
    # TODO: add shortcuts to favorite color schemes
    "color scheme": ":colorscheme ",

    # Plugins
    "toggle nerdy [tree]": LEADER + "n",
        # map <leader>n :NERDTreeToggle<CR>
    "startify": LEADER + "st",
        # map <leader>st :Startify<CR>
    "airline refresh": LEADER + "Talr", # :AirlineRefresh<CR>

    # vundle
    "plugin install": LEADER + "Tpli", # :PluginInstall<CR>
    "plugin update": LEADER + "Tplu", # :PluginUpdate<CR>
    "plugin clean": LEADER + "Tplc", # :PluginClean<CR>

    # commentary.vim
    "trundle": Key('cmd-/'),
        # nmap <D-/> gcc
        # vmap <D-/> gc

    # vim-unimpaired.vim
    "buffer previous": "[b",
    "buffer next": "]b",
    "quick previous": "[q",
    "quick next": "]q",
    "tab unimpaired previous": "[t",
    "tab unimpaired next": "]t",

    "[insert] line above": "[ ",
    "[insert] line below": "] ",
    "switchee": "[e",
    "switcho": "]e",

    "[toggle] background": "yob",
    "[toggle] cursor line": "yoc",
    "[toggle] diff this": "yod",
    "[toggle] highlight": "yoh",
    "([toggle] invisibles | toggle list)": "yol",
    "[toggle] relative": "yor",
    "toggle spell": "yos",
    "[toggle] cursor column": "you",
    "toggle wrap": "you",
    "[toggle] crosshairs": "yox",

    # buffer shortcuts
    "buffer name [<dgndictation>]": [":b ", text],
    "buffer alternate": LEADER + "Tbfa", # :b#<CR>

    # quickfix shortcuts
    "quick open": LEADER + "qo", # :cope<CR>
    "quick close": LEADER + "qc", # :ccl<CR>
    "quick max": LEADER + "qm", # :cope<CR><c-w>_

    # diff shortcuts
    "previous diff": "[c",
    "next diff": "]c",
    "diff put": "dp",
    "range diff put": LEADER + "Tdpr", # :diffp<M-Left>
    "diff (get | obtain)": "do",
    "range diff get": LEADER + "Tdgr", # :diffg<M-Left>
})
