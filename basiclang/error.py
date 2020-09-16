#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .position import Position


class Error:
    def __init__(self, pos_start: Position, pos_end: Position, error_name: str, details: str) -> None:
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
    def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
