from lark import Lark, UnexpectedInput, UnexpectedToken

from interpreter import Interpreter


def main():
    with open('grammar.g') as f:
        parser = Lark(f, start='program', parser='lalr', lexer='contextual')

    with open('test_data/04_2.lsp') as f:
        text = f.read()

    # text = '(+ 1 2 3) \n (* 4 5 6)'

    try:
        tree = parser.parse(text)
    except (UnexpectedInput, UnexpectedToken):
        print('syntax error')
    else:
        print(tree.pretty())
        Interpreter().interpret(tree)
        


if __name__ == '__main__':
    main()
