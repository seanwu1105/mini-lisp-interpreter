import io
import logging
import unittest
from unittest import mock

from mlisp import Interpreter


class TestInterpreter(unittest.TestCase):
    def test_syntax_error(self):
        code = '(+)'
        self.assertRaises(SyntaxError, Interpreter().interpret, code)
        code = '''
            (+ (* 5 2) -)


            '''
        self.assertRaises(SyntaxError, Interpreter().interpret, code)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_num(self, mock_stdout):
        code = '''
            (print-num 1)
            (print-num 2)
            (print-num 3)
            (print-num 4)
            (print-num 0)
            (print-num -123)
            (print-num 456)
            '''
        Interpreter().interpret(code)
        self.assertEqual(mock_stdout.getvalue(), '1\n2\n3\n4\n0\n-123\n456\n')

    def test_calculation(self):
        code = '''
            (+ 1 2 3)
            (* 4 5 6)
            (+ 1 (+ 2 3 4) (* 4 5 6) (/ 8 3) (mod 10 3))
            (mod 10 4)
            (- (+ 1 2) 4)
            -256
            (mod 10 (+ 1 2))
            (* (/ 1 2) 4)
            (- (+ 1 2 3 (- 4 5) 6 (/ 7 8) (mod 9 10))
                11)
            '''
        self.assertEqual(Interpreter().interpret(code),
                         [6, 120, 133, 2, -1, -256, 1, 0, 9])

    def test_bool(self):
        code = '''
            #t
            #f
            (and #t #f)
            (and #t #t)
            (or #t #f)
            (or #f #f)
            (not #t)
            (not #f)
            (or #t #t #f)
            (or #f (and #f #t) (not #f))
            (and #t (not #f) (or #f #t) (and #t (not #t)))
        '''
        self.assertEqual(Interpreter().interpret(code),
                         [True, False, False, True, True, False,
                          False, True, True, True, False])

    def test_if(self):
        code = '''
            (if #t 1 2)
            (if #f 1 2)
            (if (< 1 2) (+ 1 2 3) (* 1 2 3 4 5))
            (if (= 9 (* 2 5))
                0
                (if #t 1 2))
        '''
        self.assertEqual(Interpreter().interpret(code), [1, 2, 6, 1])

    def test_define(self):
        code = '''
            (define x 1)
            x
            (define y (+ 1 2 3))
            y
            (define a (* 1 2 3 4))
            (define b (+ 10 -5 -2 -1))
            (+ a b)
        '''
        self.assertEqual(Interpreter().interpret(code), [1, 6, 26])

    def test_anony_func(self):
        code = '''
            ((fun (x) (+ x 1)) 3)
            ((fun (a b) (+ a b)) 4 5)
            (define x 0)
            ((fun (x y z) (+ x (* y z))) 10 20 30)
            x
        '''
        self.assertEqual(Interpreter().interpret(code), [4, 9, 610, 0])

    def test_named_func(self):
        code = '''
            (define foo
                (fun (a b c) (+ a b (* b c))))
            (foo 10 9 8)
            (define bar (fun (x) (+ x 1)))
            (define bar-z (fun () 2))
            (bar (bar-z))
        '''
        self.assertEqual(Interpreter().interpret(code), [91, 3])

    def test_recursion(self):
        code = '''
            (define fact
                (fun (n) (if (< n 3) n
                             (* n (fact (- n 1))))))
            (fact 2)
            (fact 3)
            (fact 4)
            (fact 10)
            (define fib (fun (x)
                (if (< x 2) x (+
                              (fib (- x 1))
                              (fib (- x 2))))))
            (fib 1)
            (fib 3)
            (fib 5)
            (fib 10)
            (fib 20)
            (define min
                (fun (a b)
                    (if (< a b) a b)))
            (define max
                (fun (a b)
                    (if (> a b) a b)))
            (define gcd
                (fun (a b)
                    (if (= 0 (mod (max a b) (min a b)))
                        (min a b)
                        (gcd (min a b) (mod (max a b) (min a b))))))
            (gcd 100 88)
            (gcd 1234 5678)
            (gcd 81 54)
        '''
        self.assertEqual(Interpreter().interpret(code),
                         [2, 6, 24, 3628800, 1, 2, 5, 55, 6765, 4, 2, 27])

    def test_type_error(self):
        code = '(+ 1 2 3 (or #t #f))'
        self.assertRaises(TypeError, Interpreter().interpret, code)
        code = '''
            (define f
                (fun (x)
                    (if (> x 10) 10 (= x 5))))
            (* 2 (f 4))
            '''
        self.assertRaises(TypeError, Interpreter().interpret, code)

    def test_nested_func(self):
        code = '''
            (define dist-square
                (fun (x y)
                    (define square (fun (x) (* x x)))
                    (+ (square x) (square y))))
            (dist-square 3 4)
            (define diff
                (fun (a b)
                    (define abs
                    (fun (a)
                        (if (< a 0) (- 0 a) a)))
                    (abs (- a b))))
            (diff 1 10)
            (diff 10 2)
        '''
        self.assertEqual(Interpreter().interpret(code), [25, 9, 8])

    def test_first_class_func(self):
        code = '''
            (define add-x
                (fun (x) (fun (y) (+ x y))))
            (define z (add-x 10))
            (z 1)
            (define foo
                (fun (f x) (f x)))
            (foo (fun (x) (- x 1)) 10)
        '''
        self.assertEqual(Interpreter().interpret(code), [11, 9])
