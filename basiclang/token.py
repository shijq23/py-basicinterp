#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from basiclang.position import Position
import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'
TT_POW = 'TT_POW'
TT_EQ = 'EQ'

KEYWORDS = [
    'VAR'
]


class Token:
    def __init__(self, type_: str, value_=None, pos_start: Position = None, pos_end: Position = None) -> None:
        self.type = type_
        self.value = value_
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy().advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value) -> bool:
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
