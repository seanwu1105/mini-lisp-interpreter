# Lispy: Scheme Interpreter in Python

# (c) Peter Norvig, 2010-16; See http://norvig.com/lispy.html

from __future__ import division
import math
import operator as op
import functools

# Types

Symbol = str          # A Lisp Symbol is implemented as a Python str
List = list         # A Lisp List is implemented as a Python list
Number = (int, float)  # A Lisp Number is implemented as a Python int or float

# Parsing: parse, tokenize, and read_from_tokens


def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))


def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

# Environments


def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        'print-num': lambda x: print(x),
        'print-bool': lambda x: print('#t' if x else '#f'),
        '+': lambda *x: sum(x),
        '-': op.sub,
        '*': lambda *x: functools.reduce(op.mul, x, 1),
        '/': lambda x, y: int(op.truediv(x, y)),
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le,
        '=': lambda *x: all(x[0] == i for i in x),
        'mod': op.mod,
        'abs':     abs,
        'append':  op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?':     op.is_,
        'equal?':  op.eq,
        'length':  len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
        'and': lambda *x: all(x),
        'or': lambda *x: any(x)
    })
    return env


class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."

    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, name):
        "Find the innermost Env where var appears."
        if name not in self and self.outer is None:
            print("Name Error: %s is not defined" % name)
            exit(1)
        return self if name in self else self.outer.find(name)


global_env = standard_env()

# Interaction: A REPL


def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        tree = parse(input(prompt))
        print(tree)
        val = eval(tree)
        # if val is not None:
            # print(lispstr(val))


def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

# Procedures


class Procedure(object):
    "A user-defined Scheme procedure."

    def __init__(self, parms, body, env=global_env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))

# eval


def eval(node, env=global_env):
    "Evaluate an expression in an environment."
    # convert '#t' to Python True
    if node == '#t':
        return True
    # convert '#f' to Python False
    if node == '#f':
        return False
    if isinstance(node, Symbol):      # variable reference
        r = env.find(node)[node]
        return r
    elif not isinstance(node, List):  # constant literal
        return node
    elif node[0] == 'quote':          # (quote exp)
        (_, exp) = node
        return exp
    elif node[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = node
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif node[0] == 'define':         # (define var exp)
        (_, var, exp) = node
        env[var] = eval(exp, env)
    elif node[0] == 'set!':           # (set! var exp)
        (_, var, exp) = node
        env.find(var)[var] = eval(exp, env)
    elif node[0] == 'fun':         # (fun (var...) body)
        parms = node[1]
        body = node[-1]
        return Procedure(parms, body, env)
    else:                          # (proc arg...)
        proc = eval(node[0], env)
        args = tuple(eval(exp, env) for exp in node[1:])
        return proc(*args)


# tree = parse('(define bar (fun (x) (+ x 1)))')
# print(tree)
# val = eval(tree)

tree = parse('(define bar-z (fun () 2))')
print(tree)
val = eval(tree)

tree = parse('(print-num (bar-z))')
print(tree)
val = eval(tree)
