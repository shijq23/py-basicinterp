#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from basiclang.position import Position

class Context:
    def __init__(self, display_name: str, parent: Context = None, parent_entry_pos: Position = None) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parant_entry_pos = parent_entry_pos