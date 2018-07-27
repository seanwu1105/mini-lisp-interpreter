import io
import logging
import unittest
from unittest import mock

from mlisp import Interpreter


class TestInterpreter(unittest.TestCase):
    def test_syntax_error(self):
        code = r'(+)'
        self.assertRaises(SyntaxError, Interpreter().interpret, code)
        code = r'''
            (+ (* 5 2) -)


            '''
        self.assertRaises(SyntaxError, Interpreter().interpret, code)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_num(self, mock_stdout):
        code = r'''
            (print-num 1)
            (print-num 2)
            (print-num 3)
            (print-num 4)
            '''
        Interpreter().interpret(code)
        self.assertEqual(mock_stdout.getvalue(), '1\n2\n3\n4\n')
