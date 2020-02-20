from talon.voice import Word, Context, press, Key
from talon import clip

from ..utils import (
    insert,
    normalise_keys,
    parse_word,
    surround,
    text,
    sentence_text,
    word,
    parse_words,
    spoken_text,
)


def title_case_capitalize_word(index, word, _):
    words_to_keep_lowercase = "a,an,the,at,by,for,in,of,on,to,up,and,as,but,or,nor".split(
        ","
    )
    if index == 0 or word not in words_to_keep_lowercase:
        return word.capitalize()
    else:
        return word


formatters = normalise_keys(
    {
        "thrack": (True, lambda i, word, _: word[0:3] if i == 0 else ""),
        "quattro": (True, lambda i, word, _: word[0:4] if i == 0 else ""),
        "(cram | camel)": (
            True,
            lambda i, word, _: word if i == 0 else word.capitalize(),
        ),
        "pathway": (True, lambda i, word, _: word if i == 0 else "/" + word),
        "dotsway": (True, lambda i, word, _: word if i == 0 else "." + word),
        "yellsmash": (True, lambda i, word, _: word.upper()),
        "(allcaps | yeller)": (False, lambda i, word, _: word.upper()),
        "yellsnik": (
            True,
            lambda i, word, _: word.upper() if i == 0 else "_" + word.upper(),
        ),
        "dollcram": (
            True,
            lambda i, word, _: "$" + word if i == 0 else word.capitalize(),
        ),
        # "champ": (True, lambda i, word, _: word.capitalize() if i == 0 else " " + word),
        "lowcram": (
            True,
            lambda i, word, _: "@" + word if i == 0 else word.capitalize(),
        ),
        "(criff | criffed)": (True, lambda i, word, _: word.capitalize()),
        "dotcriffed": (True, lambda i, word, _: "." + word.capitalize() if i == 0 else word.capitalize()),
        "tridal": (False, lambda i, word, _: word.capitalize()),
        "snake": (True, lambda i, word, _: word if i == 0 else "_" + word),
        "dotsnik": (True, lambda i, word, _: "." + word if i == 0 else "_" + word),
        "dot": (True, lambda i, word, _: "." + word if i == 0 else "_" + word),
        "smash": (True, lambda i, word, _: word),
        "(spine | kebab)": (True, lambda i, word, _: word if i == 0 else "-" + word),
        "title": (False, title_case_capitalize_word),
    }
)

surrounders = normalise_keys(
    {
        "(surround dubstring | surround coif)": (False, surround('"')),
        "(surround string | surround posh)": (False, surround("'")),
        "(surround tics | surround glitch)": (False, surround("`")),
        "surround prank": (False, surround(" ")),
        "surround dunder": (False, surround("__")),
        "surround angler": (False, surround("<", ">")),
        "surround brisk": (False, surround("[", "]")),
        "surround kirk": (False, surround("{", "}")),
        "surround precoif": (False, surround('("', '")')),
        "surround prex": (False, surround("(", ")")),
    }
)

formatters.update(surrounders)


def FormatText(m):
    fmt = []

    for w in m._words:
        if isinstance(w, Word) and w != "over":
            fmt.append(w.word)
    words = parse_words(m)
    if not words:
        try:
            with clip.capture() as s:
                press("cmd-c")
            words = s.get().split(" ")
        except clip.NoChange:
            words = [""]

    tmp = []

    smash = False
    for i, w in enumerate(words):
        word = parse_word(w, True)
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words) - 1)
        tmp.append(word)

    sep = "" if smash else " "
    insert(sep.join(tmp))
    # if no words, move cursor inside surrounders
    if not words[0]:
        for i in range(len(tmp[0]) // 2):
            press("left")


# from ..noise import pop_control as pc

ctx = Context("formatters")
# ctx = Context("formatters", func=lambda app, window: pc.PopControl.mode != pc.PopControl.DICTATION)
ctx.keymap(
    {
        "phrase <dgndictation> [over]": spoken_text,
        "phrase <dgndictation> [tree]": [spoken_text, " tree"],
        "phrase <dgndictation> [subtree]": [spoken_text, " subtree"],

        "squash <dgndictation> [over]": text,
        "derek [<dgndictation>] [over]": [" ", spoken_text],
        "darren [<dgndictation>] [over]": [Key("cmd-right"), " ", spoken_text],
        "(sentence | champ) <dgndictation> [over]": sentence_text,
        "(comma | ,) <dgndictation> [over]": [", ", spoken_text],
        "period <dgndictation> [over]": [". ", sentence_text],
        "word <dgnwords>": word,
        "(%s)+ [<dgndictation>] [over]" % (" | ".join(formatters)): FormatText,
        # to match surrounder command + another command (i.e. not dgndictation)
        "(%s)+" % (" | ".join(surrounders)): FormatText,
    }
)


