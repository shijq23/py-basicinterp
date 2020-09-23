#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from basiclang.context import Context
from basiclang.strings_with_arrows import string_with_arrows
from basiclang.position import Position


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
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
        super().__init__(pos_start, pos_end, 'Expected Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RTError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str, context: Context) -> None:
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self) -> str:
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}\n'
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context
        while ctx:
            result = f' File {pos.fn}, line {str(pos.ln +1)}, in {ctx.display_name}\n' + result
            pos = ctx.parant_entry_pos
            ctx = ctx.parent
        return 'Tracebak (most recent call last):\n' + result
