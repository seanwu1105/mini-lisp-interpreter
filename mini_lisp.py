from lark import Lark, UnexpectedInput, UnexpectedToken

import interpreter


def main():
    with open('grammar.g') as f:
        parser = Lark(f, start='program', parser='lalr', lexer='contextual')

    with open('test_data/b1_1.lsp') as f:
        text = f.read()

    text = '(print-num (if #f 1 2))'

    try:
        tree = parser.parse(text)
    except (UnexpectedInput, UnexpectedToken):
        print('syntax error')
    else:
        print(tree.pretty())
        interpreter.interpret(tree)
        


if __name__ == '__main__':
    main()
