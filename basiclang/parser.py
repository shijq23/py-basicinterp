#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from .node import BinOpNode, NumberNode
from typing import List
from .token import TT_DIV, TT_FLOAT, TT_INT, TT_MINUS, TT_MUL, TT_PLUS, Token


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.tok_idx = -1
        self.cur_tok = None
        self.advance()

    def advance(self) -> Parser:
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.cur_tok = self.tokens[self.tok_idx]
        else:
            self.cur_tok = None
        return self

    def parse(self):
        res = self.expr()
        return res

    def factor(self) -> NumberNode:
        tok = self.cur_tok
        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)

    def term(self) -> BinOpNode:
        return self.bin_op(self.factor, (TT_DIV, TT_MUL))

    def expr(self) -> BinOpNode:
        return self.bin_op(self.term,  (TT_MINUS, TT_PLUS))

    def bin_op(self, func, ops):
        left = func()
        while self.cur_tok and self.cur_tok.type in ops:
            op_tok = self.cur_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        return left
