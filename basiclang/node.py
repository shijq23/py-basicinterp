#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from .token import Token


class NumberNode:
    def __init__(self, tok: Token) -> None:
        self.tok = tok

    def __repr__(self) -> str:
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, left_node: NumberNode, op_tok: Token, right_node: NumberNode) -> None:
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok: Token, node: NumberNode) -> None:
        self.op_tok = op_tok
        self.node = node

    def __repr__(self) -> str:
        return f'{self.op_tok}, {self.node}'
