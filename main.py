import sys

import mlisp


def main():
    mlisp.Interpreter().interpret(sys.stdin.read())


if __name__ == '__main__':
    main()
