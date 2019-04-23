from talon.voice import Key, Context, Str, press
from ..misc.basic_keys import alphabet, digits

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

def number_pi(m):
    s = m['basic_keys.digits']
    number = digits[s[0]]
    insert(number)
    press('escape')
    insert('p')
    press('escape')
    insert(' ')

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
        "cosine": ["Cos[]", Key('left')],
        "sine": ["Sin[]", Key('left')],
        "bessel jay": ["BesselJ[]", Key('left')],
        "bessel why": ["BesselY[]", Key('left')],
        "plot": ["Plot[]", Key('left')],
        "series": ["Series[]", Key('left')],
        "quantity": ["Quantity[]", Key('left')],
        "aych bar": [Key('escape'), "hb", Key('escape')],
        "infinity": [Key('escape'), "inf", Key('escape')],

        # text input shortcuts
        "simplify that": "//FullSimplify",
        "short simplify that": "//Simplify",
        "complex expand": "//ComplexExpand",
        "unit convert": "//UnitConvert",

        # greek letters
        "greek {basic_keys.alphabet}": greek,
        "upper greek {basic_keys.alphabet}": upper_greek,
        "{basic_keys.digits} pie": number_pi,

        "alpha": [Key('escape'), Key('a'), Key('escape')],
        "beta": [Key('escape'), Key('b'), Key('escape')],
        "gamma": [Key('escape'), Key('g'), Key('escape')],
        "delta": [Key('escape'), Key('d'), Key('escape')],
        "epsilon": [Key('escape'), Key('e'), Key('escape')],
        "lambda": [Key('escape'), Key('l'), Key('escape')],
        "rho": [Key('escape'), Key('r'), Key('escape')],
        "sigma": [Key('escape'), Key('s'), Key('escape')],
        "omega": [Key('escape'), Key('w'), Key('escape')],
        "chai": [Key('escape c escape')],
    }
)
