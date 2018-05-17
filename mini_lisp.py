import sys

from lark import Lark, UnexpectedInput, UnexpectedToken

import interpreter


def main():
    with open('grammar.g') as f:
        parser = Lark(f, start='program', parser='lalr', lexer='contextual')
    text = sys.stdin.read()
    try:
        tree = parser.parse(text)
    except (UnexpectedInput, UnexpectedToken):
        print('syntax error')
    else:
        interpreter.interpret(tree)


if __name__ == '__main__':
    main()
