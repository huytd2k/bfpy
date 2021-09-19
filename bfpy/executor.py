from os import read
from typing import List
from bfpy.tokenizer import Token


class Executor:
    def __init__(self, max_mem: int, tokens: List[Token]) -> None:
        self._max_mem = max_mem
        self.mems = [0] * max_mem
        self.cur_ptr_index = 0
        self.tokens = tokens
        self.cur_token_idx = 0
        self.trace_back_map_br = {}

    def handle_incr(self):
        self.mems[self.cur_ptr_index] += 1
        self._move_to(self.cur_token_idx + 1)

    def handle_decr(self):
        self.mems[self.cur_ptr_index] -= 1
        self._move_to(self.cur_token_idx + 1)

    def handle_next_ptr(self):
        self.cur_ptr_index += 1
        self._move_to(self.cur_token_idx + 1)

    def handle_prev_ptr(self):
        self.cur_ptr_index -= 1
        self._move_to(self.cur_token_idx + 1)

    def _match_token(self, a: Token, b: Token):
        return (a, b) in ((Token.OPBR, Token.CLSBR), (Token.CLSBR, Token.OPBR))

    def _find_matching_cls_br(self, op_pos: int) -> int:
        """find index of matching cls bracket"""
        cur_pos = op_pos
        stack = [self.tokens[cur_pos]]
        cur_pos += 1

        while cur_pos < len(self.tokens):
            if self.tokens[cur_pos] not in (Token.OPBR, Token.CLSBR):
                cur_pos += 1
            else:
                if self._match_token(self.tokens[cur_pos], stack[-1]):
                    stack.pop(-1)
                else:
                    stack.append(self.tokens[cur_pos])
                if len(stack) == 0:
                    return cur_pos
                cur_pos += 1

        raise ValueError("Cannot find matching close brack")

    def handle_opbr(self):
        match_br_idx = self._find_matching_cls_br(self.cur_token_idx)
        self.trace_back_map_br[match_br_idx] = self.cur_token_idx
        if self.mems[self.cur_ptr_index] == 0:
            self._move_to(match_br_idx + 1)
        else:
            self._move_to(self.cur_token_idx + 1)

    def handle_cls_br(self):
        self._move_to(self.trace_back_map_br[self.cur_token_idx])

    def _move_to(self, idx: int):
        self.cur_token_idx = idx

    def handle_eval(self):
        print(chr(self.mems[self.cur_ptr_index]), end="")
        self._move_to(self.cur_token_idx + 1)

    def handle_read(self):
        c = ord(input())
        self.mems[self.cur_ptr_index] = c
        self._move_to(self.cur_token_idx + 1)

    @property
    def cur_token(self):
        return self.tokens[self.cur_token_idx]

    def exec(self):
        while self.cur_token != Token.END:
            if self.cur_token == Token.INCR:
                self.handle_incr()
            elif self.cur_token == Token.DECR:
                self.handle_decr()
            elif self.cur_token == Token.EVAL:
                self.handle_eval()
            elif self.cur_token == Token.OPBR:
                self.handle_opbr()
            elif self.cur_token == Token.CLSBR:
                self.handle_cls_br()
            elif self.cur_token == Token.NEXTPTR:
                self.handle_next_ptr()
            elif self.cur_token == Token.PREPTR:
                self.handle_prev_ptr()
            elif self.cur_token == Token.READ:
                self.handle_read()
