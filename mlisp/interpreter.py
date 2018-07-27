import functools
import logging
import operator

from lark import Lark, UnexpectedInput, UnexpectedToken, UnexpectedCharacters


logging.basicConfig(level=logging.INFO)


class Interpreter(object):
    def __init__(self):
        self.tree = None
        with open('mlisp/grammar.lark') as larkfile:
            self.parser = Lark(larkfile, start='program',
                               parser='lalr', lexer='contextual')

    def interpret(self, code):
        try:
            self.tree = self.parser.parse(code)
        except (UnexpectedInput, UnexpectedToken, UnexpectedCharacters):
            raise SyntaxError('Mini-lisp syntax error.')
        else:
            return interpret_ast(self.tree)


class Environment(dict):
    """ The symbol table with the link if outer environment. """

    def __init__(self, symbol_names=None, symbol_values=None, outer=None):
        """Create the symbol table with local variables and functions.

        Keyword Arguments:
            symbol_names {iterable} -- The name of symbols (default: {None})
            symbol_values {iterable} -- The content of symbols (default: {None})
            outer {Environment instance} -- The outer environment (default: {None})
        """
        super().__init__(self)

        if symbol_names is None:
            symbol_names = tuple()
            symbol_values = tuple()
        self.update(zip(symbol_names, symbol_values))
        self.outer = outer

    def find(self, name):
        """ Get the innermost environment where the symbol name appears. """
        if name not in self and self.outer is None:
            raise NameError("%s is not defined" % name)
        return self if name in self else self.outer.find(name)


class GlobalEnvironment(Environment):
    """ The default symbol table. """

    def __init__(self):
        super().__init__()
        self.update({
            'print_num': print,
            'print_bool': lambda x: print('#t' if x else '#f'),
            'plus': self.plus,
            'minus': self.minus,
            'multiply': self.multiply,
            'divide': self.divide,
            'modulus': self.modulus,
            'greater': self.greater,
            'smaller': self.smaller,
            'equal': self.equal,
            'and_op': self.and_op,
            'or_op': self.or_op,
            'not_op': self.not_op
        })

    def plus(self, *args):
        self.number_type_checker(args)
        return sum(args)

    def minus(self, *args):
        self.number_type_checker(args)
        return args[0] - args[1]

    def multiply(self, *args):
        self.number_type_checker(args)
        return functools.reduce(operator.mul, args, 1)

    def divide(self, *args):
        self.number_type_checker(args)
        return int(operator.truediv(args[0], args[1]))

    def modulus(self, *args):
        self.number_type_checker(args)
        return args[0] % args[1]

    def greater(self, *args):
        self.number_type_checker(args)
        return args[0] > args[1]

    def smaller(self, *args):
        self.number_type_checker(args)
        return args[0] < args[1]

    def equal(self, *args):
        self.number_type_checker(args)
        return all(args[0] == arg for arg in args)

    def and_op(self, *args):
        self.boolean_type_checker(args)
        return all(args)

    def or_op(self, *args):
        self.boolean_type_checker(args)
        return any(args)

    def not_op(self, arg):
        self.boolean_type_checker([arg])
        return not arg

    @staticmethod
    def number_type_checker(args):
        if not all(type(arg) is int for arg in args):
            raise TypeError("Expect 'number' but got 'boolean'.")

    @staticmethod
    def boolean_type_checker(args):
        if not all(type(arg) is bool for arg in args):
            raise TypeError("Expect 'boolean' but got 'number'.")


class Function(object):
    """ A user-defined scheme function. """

    def __init__(self, args, body, environment=GlobalEnvironment()):
        self.args, self.body, self.environment = args, body, environment

    def __call__(self, *params):
        return interpret_ast(self.body, Environment(self.args, params, self.environment))


def interpret_ast(node, environment=GlobalEnvironment()):
    """ Interpret the AST of mini-lisp.

    Arguments:
        node {Tree or Token} -- The current dealing object.

    Keyword Arguments:
        environment {Environment} -- The symbol table (default: {GlobalEnvironment()})
    """

    try:  # convert SIGNED_INT to int
        return int(node)
    except (TypeError, ValueError):
        # convert '#t' to Python True
        if node == '#t':
            return True

        # convert '#f' to Python False
        if node == '#f':
            return False

        # symbol reference
        if isinstance(node, str):
            return environment.find(node)[node]

        # program : stmt+
        if node.data == 'program':
            ret = list()
            for child in node.children:
                result = interpret_ast(child, environment)
                logging.debug(result)
                if result is not None:
                    ret.append(result)
            return ret

        # if_exp : test_exp then_exp else_exp
        elif node.data == 'if_exp':
            (test, then, els) = node.children
            test_res = interpret_ast(test, environment)
            # type checking -> test_exp should be boolean
            if not isinstance(test_res, bool):
                raise TypeError("Expect 'boolean' but got 'number'.")
            expr = then if test_res else els
            return interpret_ast(expr, environment)

        # def_stmt : ( variable exp )
        elif node.data == 'def_stmt':
            (var, expr) = node.children
            environment[var] = interpret_ast(expr, environment)

        # fun_exp : ( fun_ids fun_body )
        elif node.data == 'fun_exp':
            args = interpret_ast(node.children[0])
            body = interpret_ast(node.children[-1])
            return Function(args, body, environment)

        # simply return all arguments (ids)
        elif node.data == 'fun_ids':
            return node.children

        # fun_body : def_stmt* exp
        elif node.data == 'fun_body':
            # deal with define statements
            for def_stmt in node.children[:-1]:
                interpret_ast(def_stmt)
            # return the expresion (the actual function body)
            return node.children[-1]

        # get the user-defined function with arguments and then execute it
        elif node.data == 'fun_call':
            proc = interpret_ast(node.children[0], environment)
            args = tuple(interpret_ast(expr, environment)
                         for expr in node.children[1:])
            return proc(*args)

        # execute the function got from environment dict
        else:
            proc = interpret_ast(node.data, environment)
            args = tuple(interpret_ast(expr, environment)
                         for expr in node.children)
            return proc(*args)
