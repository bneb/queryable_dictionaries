""" A currated list of approved operations for QueryDicts filtering.

See: https://docs.python.org/3/library/re.html#writing-a-tokenizer
and: https://docs.python.org/3/library/operator.html#operator.methodcaller
"""

from operator import *
import re

_UNARY_OPERATORS = {
    re.escape("not"): not_, # Negation (Logical)
}

_REVERSE_ARG_OPERATORS = {
    re.escape("in"): contains, # Containment Test
}

_BINARY_OPERATORS = {
    re.escape("is not"): is_not, # Identity
    # re.escape("+"): add, # Addition
    # re.escape("/"): truediv, # Division
    # re.escape("//"): floordiv, # Integer Division
    re.escape("&"): and_, #bitwise And
    re.escape("^"): xor, #bitwise Exclusive Or
    re.escape("|"): or_, # bitwise Or
    # re.escape("**"): pow, # Exponentiation
    re.escape("is"): is_, # Identity
    # re.escape("%"): mod, # Modulo
    # re.escape("*"): mul, # Multiplication
    # re.escape("-"): sub, # Subtraction
    re.escape("<"): lt, # Ordering
    re.escape("<="): le, # Ordering
    re.escape("=="): eq, # Equality
    re.escape("!="): ne, # Difference
    re.escape(">="): ge, # Ordering
    re.escape(">"): gt, # Ordering
}

OPS = {
    re.escape("is not"): is_not, # Identity
    re.escape("not"): not_, # Negation (Logical)
    re.escape("in"): contains, # Containment Test
    re.escape("&"): and_, #bitwise And
    re.escape("^"): xor, #bitwise Exclusive Or
    re.escape("|"): or_, # bitwise Or
    # re.escape("**"): pow, # Exponentiation
    re.escape("is"): is_, # Identity
    # re.escape("%"): mod, # Modulo
    # re.escape("*"): mul, # Multiplication
    # re.escape("-"): sub, # Subtraction
    re.escape("<"): lt, # Ordering
    re.escape("<="): le, # Ordering
    re.escape("=="): eq, # Equality
    re.escape("!="): ne, # Difference
    re.escape(">="): ge, # Ordering
    re.escape(">"): gt, # Ordering
}

def run_op(op, v1, v2=None):
    if not op: return True if v1 else False

    operator = get_operator(op)
    if operator in _UNARY_OPERATORS.values(): return operator(v1)
    elif operator in _REVERSE_ARG_OPERATORS.values(): return operator(v2, v1)
    elif operator in _BINARY_OPERATORS.values(): return operator(v1, v2)
    else: raise Exception("Bad operator: {}".format(op))

def get_operator(v): return OPS[re.escape(v)]
