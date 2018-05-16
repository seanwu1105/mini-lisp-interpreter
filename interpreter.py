import functools
import operator


class Environment(dict):
    """ The symbol table with the link if outer environment. """
    def __init__(self, symbol_names=None, symbol_values=None, outer=None):
        """Create the symbol table with local variables and functions.
        
        Keyword Arguments:
            symbol_names {iterable} -- The name of symbols (default: {None})
            symbol_values {iterable} -- The content of symbols (default: {None})
            outer {Environment instance} -- The outer environment (default: {None})
        """

        if symbol_names is None:
            symbol_names = tuple()
            symbol_values = tuple()
        self.update(zip(symbol_names, symbol_values))
        self.outer = outer

    def find(self, name):
        """ Get the innermost environment where the symbol name appears. """
        return self if name in self else self.outer.find(name)

class GlobalEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.update({
            'print_num': lambda x: print(x),
            'print_bool': lambda x: print('#t' if x else '#f'),
            'plus': lambda *x: sum(x),
            'minus': operator.sub,
            'multiply': lambda *x: functools.reduce(operator.mul, x, 1),
            'divide': lambda x, y: int(operator.truediv(x, y)),
            'modulus': operator.mod,
            'greater': operator.gt,
            'smaller': operator.lt,
            'equal': lambda *x: all(x[0] == i for i in x),
            'and_op': lambda *x: all(x),
            'or_op': lambda *x: any(x),
            'not_op': lambda x: not x
        })

class Interpreter(object):
    def interpret(self, node, environment=GlobalEnvironment()):
        try:# convert SIGNED_INT to int
            return int(node)
        except (TypeError, ValueError):
            if node == '#t':
                return True
            elif node == '#f':
                return False
            # symbol reference
            elif isinstance(node, str):
                return environment.find(node)[node]
            # deal with multiple stmts `program : stmt+`
            elif node.data == 'program':
                for child in node.children:
                    self.interpret(child, environment)
            # deal with Function or lambda
            # (fun args...)
            else:
                proc = self.interpret(node.data, environment)
                args = tuple(self.interpret(expr, environment) for expr in node.children)
                return proc(*args)
