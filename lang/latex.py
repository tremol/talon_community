from talon.voice import Key, Context, Str, press
from ..misc.basic_keys import alphabet, digits
from ..misc.vim import LEADER
from ..utils import parse_word, join_words, is_filetype

FILETYPES = (".tex",)

ctx = Context("latex", func=is_filetype(FILETYPES))

# def latex(app, win):
#     return win.doc.endswith(".tex")
# ctx = Context("latex", func=latex)

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
    insert("\\" + greek_letter.capitalize())

def number_pi(m):
    s = m['basic_keys.digits']
    number = digits[s[0]]
    insert(number + "\pi ")

zero_parameter_commands =  {
    "new item": "item ",
    "no number": "nonumber",
    "see dot": "cdot",
    "latex dots": "ldots",
    "frank": "frac",
    "fraction": "frac",
    "infinity": "infty",
    "big space": "quad ",
    "bigger space": "qquad ",
    "times": "times",
    "empty set": "varnothing",
    "maps to": "mapsto",
    "leader ell": "ell",
    # "cosine": "cos",
    # "sine": "sin",
    # "partial": "partial",
    # "nabla": "nabla",
    # "integral": "int",

    # greek shortcuts
    # "alpha": "alpha",
    # "beta": "beta",
    # "gamma": "gamma",
    # "delta": "delta",
    # "epsilon": "epsilon",
    # "lambda": "lambda",
    # "rho": "rho",
    # "sigma": "sigma",
    # "theta": "theta",
    # "chai": "chi",
    # "quicksy": "xi",
    # "omega": "omega",
    "big omega": "Omega",
}

def zero_parameter_command(m):
    s = m['latex.zero_parameter_commands']
    c = str(zero_parameter_commands[s[0]])
    insert("\\" + c)

single_parameter_commands =  {
    "square root": "sqrt",
    "text": "text",
    "new part": "part",
    "new chapter": "chapter",
    "new section": "section",
    "new subsection": "subsection",
    "new subsubsection": "subsubsection",
    "italics": "emph",
    "bold text": "textbf",
    "text bold": "textbf",
    "typewriter": "texttt",
    "calligraphy": "mathcal",
    "blackboard": "mathbb",
    "caption": "caption",
    "bold symbol": "boldsymbol",
    "overline": "overline",
    "overhat": "hat",
    "overdot": "dot",
    "double dot": "ddot",
    "triple dot": "dddot",
    "new to do": "todo",
}

def single_parameter_command(m):
    s = m['latex.single_parameter_commands']
    c = str(single_parameter_commands[s[0]])
    insert("\\" + c + "{}")
    press("left")

label_reference_commands =  {
    "section": "sec",
    "figure": "fig",
    "appendix": "app",
    "definition": "def",
    "example": "ex",
}

def label_command(m):
    s = m['latex.label_reference_commands']
    c = str(label_reference_commands[s[0]])
    b = "\\label{" + c + ":}"
    insert(b)
    press("left")

clever_reference = True

def clever_reference_on():
    global clever_reference
    clever_reference = True

def clever_reference_off():
    global clever_reference
    clever_reference = False

def reference_command(m):
    s = m['latex.label_reference_commands']
    c = str(label_reference_commands[s[0]])
    if clever_reference:
        b = "\\cref{" + c + ":}"
    else:
        b = "\\ref{" + c + ":}"
    insert(b)
    press("left")

def test(m):
    clever_reference_context.enable()

simple_environments = [
    "itemize",
    "enumerate",
    "center",
    "align",
    "definition",
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

delimiters = {
    "paren": "()",
    "bows": "()",
    "brackets": "[]",
    "braces": "{}",
    "spikes": "||",
}

def adapting_delimiters(m):
    s = m['latex.delimiters']
    d = str(delimiters[s[0]])
    if d == "{}":
        (dleft, dright) = ("\\{", "\\}")
    else:
        (dleft, dright) = (d[0], d[1])
    left = "\\left" + dleft
    right = "\\right" + dright
    insert(left + "  " + right)
    for i in " " + right:
        press("left")


ctx.keymap(
    {
        # single parameter commands
        "{latex.single_parameter_commands}": single_parameter_command,
        "{latex.zero_parameter_commands}": zero_parameter_command,

        # miscellaneous math commands
        "super": Key('^'),
        "sub": Key('_'),
        "squared": "^2",
        "cubed": "^3",
        "and approximate sign": " &\\approx ",
        "approximate sign": " \\approx ",
        "and equivalent sign": " &\\equiv ",
        "(proportional sign | prop to)": " \\propto ",
        "squiggle": " \\sim ",
        "much greater": " \\gg ",
        "much less": " \\ll ",
        "grayson": " \\gtrsim ",
        "lesson": " \\lesssim ",
        "great equal": " \geq ",
        "less equal": " \leq ",
        "crafty": " &= ",
        "damper": " & ",
        "doubles": " \\\\",
        "shelley": " \\nonumber\\\\",
        "big implies": "  \\quad \\Rightarrow \\quad  ",
        "implies": "\\Rightarrow \\quad  ",
        "leader in": " \\in ",
        "leader not in": " \\notin ",
        "leader to": " \\to ",
        "set minus": " \\setminus ",

        # delimiters
        "adapting {latex.delimiters}": adapting_delimiters,
        "small braces": ["\\{  \\}"] + 3*[Key("left")],

        # vim commands, assuming vimtex
        "tech compile": LEADER + "ll",
        "tech view": LEADER + "lv",
        "(tech error | teckers)": LEADER + "le",
        "tech contents": LEADER + "lt",
        "close that": "]]",

        # program commands
        "magic comment": ["% !TEX root = .tex"] + 4*[Key('left')],

        # formatting commands
        "[space] (lenny | Lenny)": [" $$", Key('left')],
        "(inline | double dolly)": ["$$", Key('left')],

        # colored text
        "painter text red": ["\\textcolor{red}{}", Key('left')],
        "painter text blue": ["\\textcolor{blue}{}", Key('left')],
        "painter text green": ["\\textcolor{green}{}", Key('left')],

        # new environments
        "new {latex.environments}": new_environment,
        "new <word> environment": new_custom_environment,

        # greek letters
        "(greek | greco) {basic_keys.alphabet}": greek,
        "upper (greek | greco) {basic_keys.alphabet}": upper_greek,
        "{basic_keys.digits} pie": number_pi,
        # TODO: define a function that references the names of the Greek letters directly

        # label and reference commands
        "label {latex.label_reference_commands}": label_command,
        "reference {latex.label_reference_commands}": reference_command,
        "label equation": ["\\label{eq:}", Key('left')],
        "reference equation": ["\\eqref{eq:}", Key('left')],
        "clever reference on": lambda m: clever_reference_on(),
        "clever reference off": lambda m: clever_reference_off(),
        "citation": ["\\cite{}", Key("left")],

    }
)
ctx.set_list('greek_alphabet', greek_letter_mappings.values())
ctx.set_list('environments', environments)
ctx.set_list('delimiters', delimiters)
ctx.set_list('zero_parameter_commands', zero_parameter_commands)
ctx.set_list('single_parameter_commands', single_parameter_commands)
ctx.set_list('label_reference_commands', label_reference_commands)
