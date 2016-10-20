import unittest
from collections import OrderedDict

from botlang.interpreter import BotlangSystem
from botlang.evaluation.evaluator import Primitive
from botlang.evaluation.values import BotResultValue


class BotlangTestCase(unittest.TestCase):

    def test_primitive_values(self):

        self.assertTrue(BotlangSystem.run('#t'))
        self.assertFalse(BotlangSystem.run('#f'))
        self.assertEqual(BotlangSystem.run('2'), 2)
        self.assertEqual(BotlangSystem.run('3.14'), 3.14)
        self.assertEqual(BotlangSystem.run('"hola"'), "hola")

    def test_and(self):

        self.assertTrue(BotlangSystem.run('(and #t #t)'))
        self.assertFalse(BotlangSystem.run('(and #t #f)'))
        self.assertFalse(BotlangSystem.run('(and #f #t)'))
        self.assertFalse(BotlangSystem.run('(and #f #f)'))

    def test_or(self):

        self.assertTrue(BotlangSystem.run('(or #t #t)'))
        self.assertTrue(BotlangSystem.run('(or #t #f)'))
        self.assertTrue(BotlangSystem.run('(or #f #t)'))
        self.assertFalse(BotlangSystem.run('(or #f #f)'))

    def test_if(self):

        self.assertEqual(BotlangSystem.run('(if #t 2 3)'), 2)
        self.assertEqual(BotlangSystem.run('(if #f 2 3)'), 3)
        self.assertEqual(BotlangSystem.run('(if (> 4 5) 100 200)'), 200)

    def test_primitive_application(self):

        self.assertTrue(BotlangSystem.run('(not #f)'))
        self.assertEqual(BotlangSystem.run('(sqrt 4)'), 2)
        self.assertEqual(BotlangSystem.run('(* 5 (/ 10 2))'), 25)
        self.assertEqual(BotlangSystem.run('(list 3 4 5 2 1)'), [3, 4, 5, 2, 1])
        self.assertEqual(BotlangSystem.run('(max (list 3 4 5 2 1))'), 5)
        self.assertEqual(BotlangSystem.run('(min (list 3 4 5 2 1))'), 1)
        self.assertEqual(BotlangSystem.run('(map abs (list 1 -2 3))'), [1, 2, 3])

    def test_lists(self):

        self.assertEqual(BotlangSystem.run('(list 1 2 3 4)'), [1, 2, 3, 4])
        self.assertEqual(BotlangSystem.run('\'(1 2 3 4)'), [1, 2, 3, 4])
        self.assertEqual(BotlangSystem.run('(list "1" "2")'), ['1', '2'])
        self.assertEqual(BotlangSystem.run('\'("1" "2")'), ['1', '2'])
        self.assertEqual(
            BotlangSystem.run('\'(hola chao)'),
            ['hola', 'chao']
        )
        self.assertEqual(
            BotlangSystem.run('(list "hola" "chao")'),
            ['hola', 'chao']
        )

        a_list = BotlangSystem.run('(cons (list 2 3) 1)')
        self.assertEqual(a_list, [[2, 3], 1])
        another_list = BotlangSystem.run('(cons 1 (list 2 3))')
        self.assertEqual(another_list, [1, 2, 3])

    def test_dictionaries(self):

        computed_dict = BotlangSystem.run("""
        (make-dict '[
                (holi "chao")
                (doge "wow")
                (such "much")
            ]
        )
        """)
        expected_dict = OrderedDict([
            ('holi', 'chao'),
            ('doge', 'wow'),
            ('such', 'much')
        ])
        self.assertEqual(computed_dict, expected_dict)

        computed_dict = BotlangSystem.run("""
            (make-dict (list
                    '(holi "chao")
                    '(doge "wow")
                    '(such "much")
                )
            )
            """)
        self.assertEqual(computed_dict, expected_dict)

        computed_dict = BotlangSystem.run("""
            (make-dict (list
                    (list 'holi "chao")
                    (list 'doge "wow")
                    (list 'such "much")
                )
            )
            """)
        self.assertEqual(computed_dict, expected_dict)

    def test_closures(self):

        self.assertTrue(BotlangSystem.run('((fun (x) x) #t)'))
        self.assertEqual(BotlangSystem.run(
            '((fun (x y) (+ (* x x) (* y y))) 3 4)'
        ), 25)

    def test_environment(self):

        runtime = BotlangSystem()
        bindings = {
            'x': 4,
            'hola': BotlangSystem.run('(max (list 1 3 2))'),
            '+': Primitive(lambda x, y: x * y, runtime.environment)
        }
        new_env = runtime.environment.new_environment(bindings)

        self.assertEqual(BotlangSystem.run('(- 3 x)', new_env), -1)
        self.assertEqual(BotlangSystem.run('(- 10 hola)', new_env), 7)
        self.assertEqual(BotlangSystem.run('(+ 2 3)', new_env), 6)

    def test_add_python_functions(self):

        def fibonacci(n):
            assert n >= 0

            if n == 0:
                return 0
            if n == 1:
                return 1
            return fibonacci(n - 1) + fibonacci(n - 2)

        runtime = BotlangSystem()
        runtime.environment.add_primitives({'fibo': fibonacci})
        self.assertEqual(runtime.eval('(fibo 4)'), 3)
        self.assertEqual(runtime.eval('(fibo 7)'), 13)

    def test_nesting(self):

        code = """
            (if (> (* 0.3 (+ 10 23)) 10)
                esto-no-sera-evaluado-asi-que-pico
                (and
                     (= (head (map abs (list -1 -2 -3))) 1)
                     (<= 11 (/ 100 6))
                )
             )
        """
        self.assertTrue(BotlangSystem.run(code))

    def test_define(self):

        code = """
            (define x 2)
            (define y 3)
            (+ x y)
        """
        self.assertEqual(BotlangSystem.run(code), 5)

        code = """
            (define factorial
                (fun (n)
                    (if (equal? n 0)
                        1
                        (* n (factorial (- n 1)))
                    )
                )
            )
            (factorial 5)
        """
        self.assertEqual(BotlangSystem.run(code), 120)

        code = """
            [define f
                (fun (g n)
                    [fun (x) (g (+ x n))]
                )
            ]
            [define g
                (f [fun (n) (* n n)] 2)
            ]
            [define h (g 3)]
            h
        """
        self.assertEqual(BotlangSystem.run(code), 25)

    def test_begin(self):

        code = """
            (begin
                (define x 1)
                (define y 2)
                (+ x y)
            )
        """
        self.assertEqual(BotlangSystem.run(code), 3)

    def test_local_definitions(self):

        code = """
            (local
                (
                    (f (fun (x y) (* x y)))
                    (x (* 2 3))
                )
                (f x 2)
            )
        """
        self.assertEqual(BotlangSystem.run(code), 12)

    def test_recursion(self):

        code = """
            (local
                ((factorial
                    (fun (n)
                        (if (equal? n 1)
                            n
                            (* n (factorial (- n 1)))
                        )
                    )
                ))
                (factorial 5)
            )
        """
        self.assertEqual(BotlangSystem.run(code), 120)

    def test_first_order_functions(self):

        code = """
            (begin
                (define f
                    (fun (n)
                        (fun (x) (+ n x))
                    )
                )
                (define g (f 3))

                (+ (g 3) (g 2))
            )
        """
        self.assertEqual(BotlangSystem.run(code), 11)

    def test_bot_node(self):

        code = """
            (bot-node (data)
                (node-result
                    data
                    "Holi, soy Botcito"
                    (terminal-node "HOLA")
                )
            )
        """
        node_result = BotlangSystem(
            BotlangSystem.base_environment()
        ).eval_bot(code, 'mensaje inicial')
        self.assertTrue(isinstance(node_result, BotResultValue))
        self.assertTrue(isinstance(node_result.data, dict))
        self.assertEqual(node_result.message, 'Holi, soy Botcito')
        self.assertEqual(node_result.bot_state, 'HOLA')

    def test_evaluation_state(self):

        test_dict = {'value': 0}

        def test_primitive():
            test_dict['value'] += 1
            return 'holi'

        code = """
            (bot-node (data)
                (test-primitive)
                (test-primitive)
                (node-result
                    data
                    "Holi"
                    (bot-node (data)
                        (test-primitive)
                        (node-result
                            data
                            "Chau"
                            end-node
                        )
                    )
                )
            )
        """

        environment = BotlangSystem.base_environment().add_cachable_primitives(
            {
                'test-primitive': test_primitive
            }
        )
        first_node_result = BotlangSystem(environment).eval_bot(code, 'oli bot')
        self.assertEqual(first_node_result.message, 'Holi')
        self.assertEqual(test_dict['value'], 2)

        execution_state = first_node_result.execution_state
        bot_node_steps = execution_state.bot_node_steps
        primitives_evaluations = execution_state.primitives_values
        self.assertEqual(bot_node_steps, 1)
        self.assertEqual(len(primitives_evaluations), 2)

        second_node_result = BotlangSystem(environment).eval_bot(
            code,
            'otro mensaje',
            execution_state
        )
        self.assertEqual(second_node_result.message, 'Chau')
        self.assertEqual(test_dict['value'], 3)

        execution_state = second_node_result.execution_state
        bot_node_steps = execution_state.bot_node_steps
        primitives_evaluations = execution_state.primitives_values
        self.assertEqual(bot_node_steps, 2)
        self.assertEqual(len(primitives_evaluations), 3)

    def test_add_code_definition(self):

        dsl = BotlangSystem().add_code_definition(
            'f',
            '(fun (n) [fun (x) (+ n x)])'
        )
        code = """
            (begin
                (define g (f 3))
                (+ (g 3) (g 2))
            )
        """
        self.assertEqual(dsl.eval(code), 11)
