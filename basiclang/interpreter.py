#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import math
from basiclang.context import Context
from basiclang.error import Error, RTError
from basiclang.token import TT_DIV, TT_MINUS, TT_MUL, TT_PLUS, TT_POW

from basiclang.position import Position
from basiclang.node import BinOpNode, NumberNode


class RTResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, res: RTResult):
        if res.error:
            self.error = res.error
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
        self.set_context()

    def set_pos(self, pos_start: Position = None, pos_end: Position = None) -> Number:
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context: Context = None) -> Number:
        self.context = context
        return self

    def add(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def sub(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def mul(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
    
    def pow(self, other) -> Number:
        if isinstance(other, Number):
            if isinstance(self.value, int) and isinstance(other.value, int):
                return Number(self.value ** other.value).set_context(self.context), None
            else:
                return Number(math.pow(self.value, other.value)).set_context(self.context), None

    def div(self, other) -> Number:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, 'Division by zero', self.context)
            else:
                return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self) -> str:
        return str(self.value)


class Interpreter:
    def visit(self, node, context: Context) -> RTResult:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context: Context) -> RTResult:
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node: NumberNode, context: Context) -> RTResult:
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.tok.pos_start, node.tok.pos_end))

    def visit_BinOpNode(self, node: BinOpNode, context: Context) -> RTResult:
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
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
        elif node.op_tok.type == TT_POW:
            result, error = left.pow(right)
        else:
            pass
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context: Context) -> RTResult:
        res = RTResult()
        op = res.register(self.visit(node.node, context))
        if res.error:
            return res
        if node.op_tok.type == TT_MINUS:
            op, err = op.mul(Number(-1))
        if err:
            return res.failure(err)
        else:
            return RTResult().success(op.set_pos(node.pos_start, node.pos_end))
