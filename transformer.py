import operator
import functools

from lark import Transformer


class LISPTransformer(Transformer):
    def __init__(self):
        self.variables = dict()
        self.functions = dict()

    def print_num(self, items):
        print(self.get_value(items[0]))

    def print_bool(self, items):
        print(self.get_value(items[0]))

    def plus(self, items):
        return sum(self.get_value(i) for i in items)

    def minus(self, items):
        return self.get_value(items[0]) - self.get_value(items[1])

    def multiply(self, items):
        return functools.reduce(operator.mul, (self.get_value(i) for i in items), 1)

    def divide(self, items):
        return int(self.get_value(items[0]) / self.get_value(items[1]))

    def modulus(self, items):
        return self.get_value(items[0]) % self.get_value(items[1])

    def greater(self, items):
        return '#t' if self.get_value(items[0]) > self.get_value(items[1]) else '#f'

    def smaller(self, items):
        return '#t' if self.get_value(items[0]) < self.get_value(items[1]) else '#f'

    def equal(self, items):
        return '#t' if self.get_value(items[0]) == self.get_value(items[1]) else '#f'

    def and_op(self, items):
        return '#t' if all(i == '#t' for i in items) else '#f'

    def or_op(self, items):
        return '#t' if any(i == '#t' for i in items) else '#f'

    def not_op(self, items):
        return '#t' if items[0] == '#f' else '#f'

    def if_exp(self, items):
        return items[1] if items[0] == '#t' else items[2]

    def def_stmt(self, items):
        self.variables[str(items[0])] = int(items[1])

    def get_value(self, item):
        try:    # just number
            return int(item)
        except ValueError:  # pre-defined variable
            try:
                return self.variables[str(item)]
            except KeyError:
                print('Name Error: name "{}" is not defined'.format(str(item)))
                exit(1)
