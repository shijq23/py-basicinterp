#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import List, Tuple

from .error import Error
from .token import Token
from .lexer import Lexer
from .parser import Parser


def run(fn: str, text: str) -> Tuple[List[Token], Error]:
    lexer = Lexer(fn, text)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error
