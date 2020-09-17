#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Tuple

from basiclang.error import Error
from basiclang.token import Token
from basiclang.lexer import Lexer
from basiclang.parser import Parser
from basiclang.interpreter import Interpreter

def run(fn: str, text: str) -> Tuple[List[Token], Error]:
    lexer = Lexer(fn, text)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    interpretor = Interpreter()
    res = interpretor.visit(ast.node)
    return res.value, res.error
