from talon.voice import Context, Key

ctx = Context("symbol")

keymap = {
    # simple
    "(question [mark] | questo)": "?",
    "plus": "+",
    "tilde": "~",
    "(bang | exclamation point | clamor)": "!",
    "(dollar [sign] | dolly)": "$",
    "(downscore | crunder)": "_",
    "colon": ":",
    "(lparen | [left] paren | precorp )": "(",
    "(rparen | are paren | right paren | precose)": ")",
    "(brace | left brace | kirksorp)": "{",
    "(rbrace | are brace | right brace | kirkos)": "}",
    "(angle | left angle | less than)": "<",
    "(rangle | are angle | right angle | greater than)": ">",
    "(star | asterisk)": "*",
    "pound": "#",
    "percent [sign]": "%",
    "caret": "^",
    "at sign": "@",
    "(and sign | ampersand | amper)": "&",
    "(pipe | spike)": "|",
    # "(dubquote | double quote | quatches)": '"',
    "quote": '"',
    # compound
    # Move to code shortcuts?
    # "mintwice": "--",
    # "plustwice": "++",
    # "minquall": "-=",
    # "pluqual": "+=",
    # "starqual": "*=",
    "double prime": "''",
    "double tick": "``",
    "triple prime": "'''",
    "triple tick": "```",
    "[forward] dubslash": "//",
    "coal twice": "::",
    "(dot dot | dotdot)": "..",
    "(ellipsis | dot dot dot | dotdotdot)": "...",
    # unnecessary: use repetition commands?

    "coif": ['""', Key("left")],
    "posh": ["''", Key("left")],
    # "(surround tics | surround glitch)": (False, surround("`")),
    "prank": ["  ", Key("left")],
    # "surround dunder": (False, surround("__")),
    # "surround angler": (False, surround("<", ">")),
    "brisk": ["[]", Key("left")],
    "kirk": ["{}", Key("left")],
    # "surround precoif": (False, surround('("', '")')),
    "prex": ["()", Key("left")],
}

ctx.keymap(keymap)
