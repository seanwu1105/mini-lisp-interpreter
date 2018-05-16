import operator
import functools

from lark import Transformer


class Interpreter(Transformer):
    def __init__(self):
        self.glob_scope = dict()

    def signed_int(self, items):
        return int(items[0])

    def bool_val(self, items):
        return True if items[0] == '#t' else False

    def print_num(self, items):
        print(items[0])

    def print_bool(self, items):
        print('#t' if items[0] else '#f')

    def plus(self, items):
        return sum(i for i in items)

    def minus(self, items):
        return items[0] - items[1]

    def multiply(self, items):
        return functools.reduce(operator.mul, items, 1)

    def divide(self, items):
        return int(items[0] / items[1])

    def modulus(self, items):
        return items[0] % items[1]

    def greater(self, items):
        return items[0] > items[1]

    def smaller(self, items):
        return items[0] < items[1]

    def equal(self, items):
        return all(items[0] == i for i in items)

    def and_op(self, items):
        return all(items)

    def or_op(self, items):
        return any(items)

    def not_op(self, items):
        return not items[0]

    def if_exp(self, items):
        return items[1] if items[0] else items[2]

    def def_stmt(self, items):
        self.glob_scope[items[0]] = items[1]

    def new_variable(self, items):
        return str(items[0])

    def variable(self, items):
        val = self.glob_scope.get(str(items[0]))
        if val is None:
            print('Name Error: variable "%s" is not defined' % str(items[0]))
            exit(1)
        else:
            return val

    def anony_fun_call(self, items):
        print("WTF")
