#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from basiclang.error import Error, RTError
from os import error
from basiclang.token import TT_DIV, TT_MINUS, TT_MUL, TT_PLUS

from basiclang.position import Position
from basiclang.node import BinOpNode, NumberNode


class RTResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = error
        return res.value

    def success(self, value: Number) -> RTResult:
        self.value = value
        return self

    def failure(self, error: Error) -> RTResult:
        self.error = error
        return self


class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start: Position = None, pos_end: Position = None) -> Number:
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def add(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value + other.value), None

    def sub(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value - other.value), None

    def mul(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    def div(self, other) -> Number:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, 'Division by zero')
            else:
                return Number(self.value / other.value), None

    def __repr__(self) -> str:
        return str(self.value)


class Interpreter:
    def visit(self, node) -> RTResult:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node) -> RTResult:
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node: NumberNode) -> RTResult:
        return RTResult().success(Number(node.tok.value).set_pos(node.tok.pos_start, node.tok.pos_end))

    def visit_BinOpNode(self, node: BinOpNode) -> RTResult:
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node))
        if res.error:
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.add(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.sub(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.mul(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.div(right)
        else:
            pass
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node) -> RTResult:
        res = RTResult()
        op = res.register(self.visit(node.node))
        if res.error:
            return res
        if node.op_tok.type == TT_MINUS:
            op, err = op.mul(Number(-1))
        if err:
            return res.failure(err)
        else:
            return RTResult().success(op.set_pos(node.pos_start, node.pos_end))
