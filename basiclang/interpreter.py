#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from basiclang.rtresult import Number, RTResult
import math
from basiclang.context import Context
from basiclang.error import Error, RTError
from basiclang.token import TT_DIV, TT_MINUS, TT_MUL, TT_PLUS, TT_POW

from basiclang.position import Position
from basiclang.node import BinOpNode, NumberNode, VarAccessNode, VarAssignNode


class Interpreter:
    def visit(self, node, context: Context) -> RTResult:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context: Context) -> RTResult:
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node: NumberNode, context: Context) -> RTResult:
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.tok.pos_start, node.tok.pos_end))

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context) -> RTResult:
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(node.pos_start, node.pos_end, f"'{var_name}' is not defined", context))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node: VarAssignNode, context: Context) -> RTResult:
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

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
