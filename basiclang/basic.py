#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from basiclang.context import SymbolTable
from typing import List, Tuple

from basiclang.error import Error
from basiclang.token import Token
from basiclang.lexer import Lexer
from basiclang.parser import Parser
from basiclang.interpreter import Context, Interpreter, Number

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))


def run(fn: str, text: str) -> Tuple[List[Token], Error]:
    lexer = Lexer(fn, text)
    tokens, error = lexer.get_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpretor = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    res = interpretor.visit(ast.node, context)
    return res.value, res.error
