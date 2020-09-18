#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from basiclang.error import Error, InvalidSyntaxError
from .node import BinOpNode, NumberNode, UnaryOpNode
from typing import List
from .token import TT_DIV, TT_EOF, TT_FLOAT, TT_INT, TT_LPAREN, TT_MINUS, TT_MUL, TT_PLUS, TT_POW, TT_RPAREN, Token


class ParserResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParserResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node) -> ParserResult:
        self.node = node
        return self

    def failure(self, error: Error) -> ParserResult:
        self.error = error
        return self


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.tok_idx = -1
        self.cur_tok = None
        self.advance()

    def advance(self) -> Token:
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.cur_tok = self.tokens[self.tok_idx]
        return self.cur_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.cur_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.cur_tok.pos_start, self.cur_tok.pos_end,
                                                  "Expected '+', '-', '*', or '/'"))
        return res

    def atom(self) -> NumberNode:
        res = ParserResult()
        tok = self.cur_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.cur_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.cur_tok.pos_start, self.cur_tok.pos_end, "Exected ')'"))

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, +, - or ("))

    def factor(self) -> NumberNode:
        res = ParserResult()
        tok = self.cur_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        return self.power()

    def term(self) -> BinOpNode:
        return self.bin_op(self.power, (TT_DIV, TT_MUL))

    def expr(self) -> BinOpNode:
        return self.bin_op(self.term,  (TT_MINUS, TT_PLUS))

    def power(self) -> BinOpNode:
        return self.bin_op(self.atom, (TT_POW), self.factor)

    def bin_op(self, func_left, ops, func_right=None) -> BinOpNode:
        if func_right == None:
            func_right = func_left
        res = ParserResult()
        left = res.register(func_left())
        if res.error:
            return res
        while self.cur_tok and self.cur_tok.type in ops:
            op_tok = self.cur_tok
            res.register(self.advance())
            right = res.register(func_right())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)
