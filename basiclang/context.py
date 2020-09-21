#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from basiclang.position import Position


class Context:
    def __init__(self, display_name: str, parent: Context = None, parent_entry_pos: Position = None) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parant_entry_pos = parent_entry_pos
        self.symbol_table = SymbolTable()


class SymbolTable:
    def __init__(self) -> None:
        self.symbols: dict = {}
        self.parent: SymbolTable = None

    def get(self, name: str):
        val = self.symbols.get(name, None)
        if val == None and self.parent != None:
            return self.parent.get(name)
        return val

    def set(self, name: str, value) -> None:
        self.symbols[name] = value

    def remove(self, name: str) -> None:
        del self.symbols[name]
