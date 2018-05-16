from lark import Lark, UnexpectedInput, UnexpectedToken

from interpreter import Interpreter


def main():
    with open('grammar.g') as f:
        parser = Lark(f, start='program', parser='lalr', lexer='contextual')

    with open('test_data/06_1.lsp') as f:
        text = f.read()

    text = '((fun (x) (+ x 1)) 3)'

    try:
        tree = parser.parse(text)
    except (UnexpectedInput, UnexpectedToken):
        print('syntax error')
    else:
        print(tree.pretty())
        


if __name__ == '__main__':
    main()
