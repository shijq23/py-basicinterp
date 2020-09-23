#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Tuple

from .token import DIGITS, KEYWORDS, LETTERS, LETTERS_DIGITS, TT_EE, TT_EOF, TT_EQ, TT_GT, TT_GTE, TT_IDENTIFIER, TT_KEYWORD, TT_LT, TT_LTE, TT_NE, TT_POW
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
from .error import Error, IllegalCharError, ExpectedCharError


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
            elif self.cur_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.cur_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.cur_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.cur_char == '=':
                tokens.append(self.make_equals())
            elif self.cur_char == '!':
                tok, err = self.make_not_equals()
                if err:
                    return [], err
                tokens.append(tok)
            elif self.cur_char == '<':
                tokens.append(self.make_less_than())
            elif self.cur_char == '>':
                tokens.append(self.make_greater_than())
            else:
                pos_start = self.pos.copy()
                char = self.cur_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self) -> Token:
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.cur_char != None and self.cur_char in DIGITS + '.':
            if self.cur_char == '.':
                if dot_count > 0:
                    break
                dot_count += 1
            num_str += self.cur_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self) -> Token:
        id_str = ''
        pos_start = self.pos.copy()

        while self.cur_char != None and self.cur_char in LETTERS_DIGITS:
            id_str += self.cur_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self) -> Token:
        pos_start = self.pos.copy()
        self.advance()

        if self.cur_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self) -> Token:
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()
        if self.cur_char == '=':
            self.advance()
            tok_type = TT_EE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self) -> Token:
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()
        if self.cur_char == '=':
            self.advance()
            tok_type = TT_GTE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self) -> Token:
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()
        if self.cur_char == '=':
            self.advance()
            tok_type = TT_LTE
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
