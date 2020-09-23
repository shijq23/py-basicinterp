#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from basiclang.error import Error, InvalidSyntaxError
from .node import BinOpNode, NumberNode, UnaryOpNode, VarAccessNode, VarAssignNode
from typing import List, Tuple
from .token import TT_DIV, TT_EE, TT_EOF, TT_EQ, TT_FLOAT, TT_GT, TT_GTE, TT_IDENTIFIER, TT_INT, TT_KEYWORD, TT_LPAREN, TT_LT, TT_LTE, TT_MINUS, TT_MUL, TT_NE, TT_PLUS, TT_POW, TT_RPAREN, Token


class ParserResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res: ParserResult):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node) -> ParserResult:
        self.node = node
        return self

    def failure(self, error: Error) -> ParserResult:
        if not self.error or self.advance_count == 0:
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
                                                  "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', '<=', '>=', 'AND', 'OR'"))
        return res

    def atom(self) -> NumberNode:
        res = ParserResult()
        tok = self.cur_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()

            return res.success(NumberNode(tok))
        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()

            return res.success(VarAccessNode(tok))
        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            if self.cur_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()

                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.cur_tok.pos_start, self.cur_tok.pos_end, "Exected ')'"))

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, identifier, +, - or ("))

    def factor(self) -> NumberNode:
        res = ParserResult()
        tok = self.cur_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()

            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        return self.power()

    def term(self) -> BinOpNode:
        return self.bin_op(self.factor, (TT_DIV, TT_MUL))

    def comp_expr(self):
        res = ParserResult()

        if self.cur_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.cur_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))
        node = res.register(self.bin_op(
            self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(self.cur_tok.pos_start, self.cur_tok.pos_end, "Expected int, float, identifier, +, -, (, NOT"))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def expr(self) -> BinOpNode:
        res = ParserResult()
        if self.cur_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.cur_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.cur_tok.pos_start, self.cur_tok.pos_end, "Expected identifier"))
            var_name = self.cur_tok

            res.register_advancement()
            self.advance()

            if self.cur_tok.type != TT_EQ:
                return res.failue(InvalidSyntaxError(self.cur_tok.pos_start, self.cur_tok.pos_end, "Expected '='"))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(
            self.comp_expr,  ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))
        if res.error:
            return res.failure(InvalidSyntaxError(self.cur_tok.pos_start, self.cur_tok.pos_end, "Expected 'VAR', int, float, identifier, +, - or ("))
        return res.success(node)

    def power(self) -> BinOpNode:
        return self.bin_op(self.atom, (TT_POW,), self.factor)

    def bin_op(self, func_left: function, ops: Tuple, func_right=None) -> BinOpNode:
        if func_right == None:
            func_right = func_left
        res = ParserResult()
        left = res.register(func_left())
        if res.error:
            return res
        while self.cur_tok.type in ops or (self.cur_tok.type, self.cur_tok.value) in ops:
            op_tok = self.cur_tok
            res.register_advancement()
            self.advance()

            right = res.register(func_right())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)
