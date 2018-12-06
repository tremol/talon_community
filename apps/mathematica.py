from talon.voice import Key, Context, Str, press
from ..misc.basic_keys import alphabet

def insert(s):
    Str(s)(None)

def greek(m):
    s = m['basic_keys.alphabet']
    press('escape')
    insert(alphabet[s[0]])
    press('escape')

def upper_greek(m):
    s = m['basic_keys.alphabet']
    press('escape')
    insert(alphabet[s[0]].upper())
    press('escape')


ctx = Context("Mathematica", bundle="com.wolfram.Mathematica")
ctx.keymap(
    {
        # commands
        "super": Key('ctrl-6'),
        "sub": Key('ctrl--'),
        "square root": Key('ctrl-2'),
        "(fraction | frank)": Key('ctrl-/'),
        "squared": [Key('ctrl-6'), Key('2'), Key('right')],
        "cubed": [Key('ctrl-6'), Key('3'), Key('right')],

        # text input shortcuts
        "simplify that": "//FullSimplify",
        "short simplify that": "//Simplify",
        "complex expand": "//ComplexExpand",

        # greek letters
        "greek {basic_keys.alphabet}": greek,
        "upper greek {basic_keys.alphabet}": upper_greek,
        "alpha": [Key('escape'), Key('a'), Key('escape')],
        "beta": [Key('escape'), Key('b'), Key('escape')],
        "gamma": [Key('escape'), Key('g'), Key('escape')],
        "lambda": [Key('escape'), Key('l'), Key('escape')],
        "sigma": [Key('escape'), Key('s'), Key('escape')],
        "omega": [Key('escape'), Key('w'), Key('escape')],
    }
)
