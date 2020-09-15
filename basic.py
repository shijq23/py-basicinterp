#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    def __init__(self, error_name, details) -> None:
        self.error_name = error_name
        self.details = details

    def as_str(self) -> str:
        result = f'{self.error_name}: {self.details}'
        return result


class IllegalCharError(Error):
    def __init__(self, details) -> None:
        super().__init__('Illegal Character', details)


class Token:
    def __init__(self, type_, value_=None) -> None:
        self.type = type_
        self.value = value_

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.pos = -1
        self.cur_char = None
        self.advance()

    def advance(self) -> None:
        self.pos += 1
        self.cur_char = self.text[self.pos] if self.pos < len(
            self.text) else None

    def get_tokens(self) -> List[Token]:
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
                char = self.cur_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")

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

def run(text) -> Tuple[List[Token], Error]:
    lexer = Lexer(text)
    tokens, error = lexer.get_tokens()
    return tokens, error
