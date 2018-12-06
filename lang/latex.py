from talon.voice import Key, Context, Str, press
from ..misc.basic_keys import alphabet
from ..utils import parse_word, join_words

def latex(app, win):
    return win.doc.endswith(".tex")

def insert(s):
    Str(s)(None)

greek_letter_mappings =  {
    "a": "alpha",
    "b": "beta",
    "g": "gamma",
    "d": "delta",
    "e": "epsilon",
    "z": "zeta",
    "h": "eta",
    "q": "theta",
    "i": "iota",
    "k": "kappa",
    "l": "lambda",
    "m": "mu",
    "n": "nu",
    "x": "xi",
    "o": "omicron",
    "p": "pi",
    "r": "rho",
    "s": "sigma",
    "t": "tau",
    "u": "upsilon",
    "f": "phi",
    "c": "chi",
    "y": "psi",
    "w": "omega",
}

def greek(m):
    s = m['basic_keys.alphabet']
    letter = alphabet[s[0]]
    greek_letter = greek_letter_mappings[letter]
    insert("\\" + greek_letter)

def upper_greek(m):
    s = m['basic_keys.alphabet']
    letter = alphabet[s[0]]
    greek_letter = greek_letter_mappings[letter]
    insert("\\" + greek_letter.upper())

simple_environments = [
    "itemize",
    "enumerate",
    "center",
    "align",
    # "minipage",
]

alias_environments = {
    "equation": "align",
}

environments = {e: e for e in simple_environments}
environments.update(alias_environments)

def new_environment(m):
    s = m['latex.environments']
    env = str(environments[s[0]])
    insert("\n\\begin{" + env + "}\n\n\\end{" + env + "}")
    # press("up")
    press("up")
    press("tab")

def new_custom_environment(m):
    try:
        text = str(list(map(parse_word, m.word[0]))[0])
    except AttributeError:
        text = 'ENVIRONMENT'

    insert("\n\\begin{" + text + "}\n\n\\end{" + text + "}")
    press("up")
    press("tab")


ctx = Context("latex", func=latex)

ctx.keymap(
    {
        # small math commands
        "super": Key('^'),
        "sub": Key('_'),
        "square root": ["\\sqrt{}", Key('left')],
        "(fraction | frank)": ["\\frac{}", Key('left')],
        "squared": "^2",
        "cubed": "^3",

        # program commands
        "(compile | shay brov)": Key('cmd-alt-b'),

        # formatting commands
        "(inline | lenny)": "$", #["$$", Key('left')],
        "new section": ["\\section{}", Key('left')],
        "new subsection": ["\\subsection{}", Key('left')],
        "new subsubsection": ["\\subsubsection{}", Key('left')],
        "new item": "\\item ",
        "italics": ["\\emph{}", Key('left')],
        "bold text": ["\\textbf{}", Key('left')],

        # new environments
        "new {latex.environments}": new_environment,
        "new <word> environment": new_custom_environment,

        # greek letters (TO DO: collapse the individuals into a word list)
        "(greek | greco) {basic_keys.alphabet}": greek,
        "upper (greek | greco) {basic_keys.alphabet}": upper_greek,
        "alpha": "\\alpha",
        "beta": "\\beta",
        "gamma": "\\gamma",
        "lambda": "\\lambda",
        "sigma": "\\sigma",
        "theta": "\\theta",
        "omega": "\\omega",
    }
)
ctx.set_list('greek_alphabet', greek_letter_mappings.values())
ctx.set_list('environments', environments)
