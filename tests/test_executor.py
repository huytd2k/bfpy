import pytest
from bfpy.executor import Executor
from bfpy.tokenizer import tokenizer
from unittest import TestCase


class TestExecutor(TestCase):
    def test_find_matching_cls_br(self):
        tokens = tokenizer("[]")
        executor = Executor(100, tokens)
        match_idx = executor._find_matching_cls_br(0)
        assert match_idx == 1

        tokens = tokenizer("[[]-]")
        executor = Executor(100, tokens)
        match_idx = executor._find_matching_cls_br(0)
        assert match_idx == 4

        tokens = tokenizer("[")
        executor = Executor(100, tokens)

        with pytest.raises(ValueError):
            match_idx = executor._find_matching_cls_br(0)

    def test_exec(self):
        tokens = tokenizer("[]")
        executor = Executor(100, tokens)
        executor.exec()
