import sys
import mini_lisp_interpreter


def main():
    mini_lisp_interpreter.Interpreter().interpret(sys.stdin.read())


if __name__ == '__main__':
    main()
