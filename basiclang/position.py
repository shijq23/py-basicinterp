#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations


class Position:
    def __init__(self, idx: int, ln: int, col: int, fn: str, ftxt: str) -> None:
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, cur_char: str = None) -> Position:
        self.idx += 1
        self.col += 1

        if cur_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self) -> Position:
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
