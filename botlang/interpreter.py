import inspect
import os

from botlang.environment import *
from botlang.evaluation.evaluator import Evaluator
from botlang.evaluation.values import BotNodeValue
from botlang.exceptions.exceptions import *
from botlang.extensions.storage import LocalStorageExtension, \
    GlobalStorageExtension, CacheExtension
from botlang.macros.macro_expander import MacroExpander
from botlang.modules.resolver import ModuleResolver
from botlang.parser import Parser


class BotlangSystem(object):

    def __init__(self, environment=None, module_resolver=None):

        if module_resolver:
            environment = module_resolver.environment

        if not environment:
            environment = self.base_environment()

        if not module_resolver:
            module_resolver = ModuleResolver(environment)

        self.environment = environment
        self.module_resolver = module_resolver

    @classmethod
    def base_environment(cls):

        env = Environment()
        return BotlangPrimitives.populate_environment(env)

    @classmethod
    def bot_modules_resolver(cls, environment):

        from botlang.modules import bot_helpers
        helpers_path = os.path.dirname(inspect.getfile(bot_helpers))

        module_resolver = ModuleResolver(environment)
        module_resolver.load_modules(helpers_path)
        return module_resolver

    @classmethod
    def bot_instance(cls, module_resolver=None):

        environment = cls.base_environment()

        if module_resolver is None:
            module_resolver = cls.bot_modules_resolver(environment)

        return BotlangSystem(module_resolver=module_resolver)

    def setup_cache_extension(self, cache_implementation):

        return CacheExtension.apply(self, cache_implementation)

    def setup_local_storage(self, db_implementation):

        return LocalStorageExtension.apply(self, db_implementation)

    def setup_global_storage(self, db_implementation):

        return GlobalStorageExtension.apply(self, db_implementation)

    def parse(self, code_string, source_id):

        ast_seq = Parser.parse(code_string, source_id)
        expanded_asts = self.expand_macros(ast_seq)
        return expanded_asts

    def expand_macros(self, ast_seq):

        from botlang.macros.default_macros import DefaultMacros
        macro_environment = DefaultMacros.get_environment()
        expanded_asts = [
            ast.accept(MacroExpander(), macro_environment) for ast in ast_seq
        ]
        return expanded_asts

    def primitive_eval(self, code_string, evaluator, source_id):

        expanded_asts = self.parse(code_string, source_id)
        return self.primitive_eval_ast(expanded_asts, evaluator)

    def primitive_eval_ast(self, ast_seq, evaluator):

        return self.interpret(ast_seq, evaluator, self.environment)

    def eval(self, code_string, source_id=None):

        evaluator = Evaluator(module_resolver=self.module_resolver)
        return self.primitive_eval(code_string, evaluator, source_id)

    def eval_bot(
            self,
            bot_code,
            input_msg,
            next_node=None,
            data=None,
            source_id=None
    ):
        ast_seq = self.parse(bot_code, source_id)
        return self.eval_bot_ast(ast_seq, input_msg, next_node, data)

    def eval_bot_ast(
            self,
            bot_ast,
            input_msg,
            next_node=None,
            data=None
    ):
        if data is None:
            data = {}

        self.environment.last_input_message = input_msg     # Legacy
        evaluator = Evaluator(module_resolver=self.module_resolver)
        result = self.primitive_eval_ast(bot_ast, evaluator)

        if next_node:
            return self.environment.lookup(next_node).apply(data, input_msg)
        if isinstance(result, BotNodeValue):
            return result.apply(data, input_msg)
        return result

    @classmethod
    def interpret(cls, ast_seq, evaluator, environment):

        try:
            for ast in ast_seq[0:-1]:
                ast.accept(evaluator, environment)
            return ast_seq[-1].accept(evaluator, environment)
        except BotlangAssertionException as failed_assert:
            raise failed_assert
        except Exception as e:
            raise BotlangErrorException(
                e,
                evaluator.execution_stack
            )

    @classmethod
    def run(
            cls,
            code_string,
            environment=None,
            module_resolver=None,
            source_id=None
    ):
        return BotlangSystem(environment, module_resolver).eval(
            code_string,
            source_id
        )
