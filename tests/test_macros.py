from unittest import TestCase

from botlang import BotlangSystem


class MacrosTestCase(TestCase):

    def test_syntax_rule(self):

        code = """
        (define-syntax-rule (my-and x y)
            (if x
                (if y #t #f)
                #f
            )
        )
        (my-and (> 5 3) (< -1 8))
        """
        result = BotlangSystem.run(code)
        self.assertTrue(result)

    def test_defun_macro(self):

        code = """
        (define-syntax-rule (def-fun name args body)
            (define name (function args body))
        )
        (def-fun squared (x) (* x x))
        (squared 4)
        """
        result = BotlangSystem.run(code)
        self.assertEqual(result, 16)

    def test_syntax_rule_hygiene(self):

        code = """
        (define-syntax-rule (my-and x y)
            (if x
                (if y #t #f)
                #f
            )
        )
        (define y #t)
        (my-and y #f) ;; Yields #t if expansion is not hygienic
        """
        result = BotlangSystem.run(code)
        self.assertFalse(result)
