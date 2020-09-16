#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Tuple

DIGITS = '0123456789'

TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


class Error:
    def __init__(self, pos_start:Position, pos_end:Position, error_name:str, details:str) -> None:
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_str(self) -> str:
        result = f'{self.error_name}: {self.details}'
        result += f' file {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += f' col {self.pos_start.col + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start:Position, pos_end:Position, details:str) -> None:
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class Position:
    def __init__(self, idx:int, ln:int, col:int, fn:str, ftxt:str) -> None:
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, cur_char:str) -> Position:
        self.idx += 1
        self.col += 1

        if cur_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self) -> Position:
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Token:
    def __init__(self, type_, value_=None) -> None:
        self.type = type_
        self.value = value_

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, fn:str, text:str) -> None:
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


def run(fn:str, text:str) -> Tuple[List[Token], Error]:
    lexer = Lexer(fn, text)
    tokens, error = lexer.get_tokens()
    return tokens, error
