from lark import Lark, UnexpectedInput, UnexpectedToken

from transformer import LISPTransformer


def main():
    with open('grammar.g') as f:
        parser = Lark(f, start='program', parser='lalr', lexer='contextual')

    with open('test_data/06_2.lsp') as f:
        text = f.read()

    try:
        tree = parser.parse(text)
    except (UnexpectedInput, UnexpectedToken):
        print('syntax error')
    else:
        print(tree.pretty())
        res = LISPTransformer().transform(tree)
        print()
        print()
        print(res)


if __name__ == '__main__':
    main()
