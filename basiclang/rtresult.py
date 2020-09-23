#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import math

from basiclang.error import Error, RTError

from basiclang.context import Context
from basiclang.position import Position


class RTResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, res: RTResult):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value: Number) -> RTResult:
        self.value = value
        return self

    def failure(self, error: Error) -> RTResult:
        self.error = error
        return self


class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start: Position = None, pos_end: Position = None) -> Number:
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context: Context = None) -> Number:
        self.context = context
        return self

    def add(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def sub(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def mul(self, other) -> Number:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def pow(self, other) -> Number:
        if isinstance(other, Number):
            if isinstance(self.value, int) and isinstance(other.value, int):
                return Number(self.value ** other.value).set_context(self.context), None
            else:
                return Number(math.pow(self.value, other.value)).set_context(self.context), None

    def div(self, other) -> Number:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, 'Division by zero', self.context)
            else:
                return Number(self.value / other.value).set_context(self.context), None

    def comp_eq(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def comp_ne(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def comp_lt(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def comp_gt(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def comp_lte(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def comp_gte(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def and_(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def or_(self, other) -> Number:
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

    def not_(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self) -> Number:
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return str(self.value)
