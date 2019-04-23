from talon.voice import Word, Context, press
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
    is_not_vim,
    is_vim,
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
        "tree": (True, lambda i, word, _: word[0:3] if i == 0 else ""),
        "quad": (True, lambda i, word, _: word[0:4] if i == 0 else ""),
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
        "champ": (False, lambda i, word, _: word.capitalize() if i == 0 else word),
        "lowcram": (
            True,
            lambda i, word, _: "@" + word if i == 0 else word.capitalize(),
        ),
        "(criff | criffed)": (True, lambda i, word, _: word.capitalize()),
        "tridal": (False, lambda i, word, _: word.capitalize()),
        "snake": (True, lambda i, word, _: word if i == 0 else "_" + word),
        "dotsnik": (True, lambda i, word, _: "." + word if i == 0 else "_" + word),
        "smash": (True, lambda i, word, _: word.lower()), # remove spaces and lowercase everything
        "lowercase": (False, lambda i, word, _: word.lower()), # lowercase everything, keeping spaces
        "(spine | kebab)": (True, lambda i, word, _: word if i == 0 else "-" + word),
        "title": (False, title_case_capitalize_word),
    }
)

surrounders = normalise_keys(
    {
        "(dubstring | coif)": (False, surround('"')),
        "(string | posh)": (False, surround("'")),
        "(tics | glitch)": (False, surround("`")),
        "(padded | prank)": (False, surround(" ")),
        "dunder": (False, surround("__")),
        "angler": (False, surround("<", ">")),
        "brisk": (False, surround("[", "]")),
        "kirk": (False, surround("{", "}")),
        "precoif": (False, surround('("', '")')),
        "(prex | args)": (False, surround("(", ")")),
    }
)

formatters.update(surrounders)


def FormatText(m, vim=False):
    fmt = []

    for w in m._words:
        if isinstance(w, Word) and w != "over":
            fmt.append(w.word)
    words = parse_words(m, True) # add True so champ preserves natural capitalization
    if not words:
        if not vim:
            try:
                with clip.capture() as s:
                    press("cmd-c")
                words = s.get().split(" ")
            except clip.NoChange:
                words = [""]
        else:
            words = [""]

    tmp = []

    smash = False
    for i, w in enumerate(words):
        word = parse_word(w, False) # change to False so champ preserves natural capitalization
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

universal_formatters_keymap = {
        "(phrase) <dgndictation> [over]": spoken_text, # changed from text to spoken_text for natural capitalization
        "sentence <dgndictation> [over]": sentence_text,
        "(comma | ,) <dgndictation> [over]": [", ", spoken_text],
        "period <dgndictation> [over]": [". ", sentence_text],
        "word <dgnwords>": word,
}

ctx = Context("formatters_not_vim", func=is_not_vim)

ctx.keymap(
    {
        **universal_formatters_keymap,
        "(%s)+ [<dgndictation>] [over]" % (" | ".join(formatters)): FormatText,
        # to match surrounder command + another command (i.e. not dgndictation)
        "(%s)+" % (" | ".join(surrounders)): FormatText,
    }
)

ctx = Context("formatters_vim", func=is_vim)

ctx.keymap(
    {
        **universal_formatters_keymap,
        "(%s)+ [<dgndictation>] [over]" % (" | ".join(formatters)): lambda m: FormatText(m, vim=True),
        # to match surrounder command + another command (i.e. not dgndictation)
        "(%s)+" % (" | ".join(surrounders)): lambda m: FormatText(m, vim=True),
    }
)
