#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Tuple

from .token import DIGITS
from .token import TT_PLUS
from .token import TT_MINUS
from .token import TT_MUL
from .token import TT_DIV
from .token import TT_LPAREN
from .token import TT_RPAREN
from .token import TT_INT
from .token import TT_FLOAT
from .token import Token
from .position import Position
from .error import Error, IllegalCharError


class Lexer:
    def __init__(self, fn: str, text: str) -> None:
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.cur_char = None
        self.advance()

    def advance(self) -> Lexer:
        self.pos.advance(self.cur_char)
        self.cur_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None
        return self

    def get_tokens(self) -> Tuple[List[Token], Error]:
        tokens = []
        while self.cur_char != None:
            if self.cur_char in ' \t':
                self.advance()
            elif self.cur_char in DIGITS + '.':
                tokens.append(self.make_number())
            elif self.cur_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.cur_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.cur_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.cur_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.cur_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.cur_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.cur_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self) -> Token:
        num_str = ''
        dot_count = 0

        while self.cur_char != None and self.cur_char in DIGITS + '.':
            if self.cur_char == '.':
                if dot_count > 0:
                    break
                dot_count += 1
            num_str += self.cur_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))