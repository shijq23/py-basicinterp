#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from error import Error
from .token import Token

from lexer import Lexer
from typing import List, Tuple


def run(fn: str, text: str) -> Tuple[List[Token], Error]:
    lexer = Lexer(fn, text)
    tokens, error = lexer.get_tokens()
    return tokens, error
