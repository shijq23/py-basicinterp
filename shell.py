#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import basic

while True:
    text = input("basic > ")
    tokens, error = basic.run(text)

    if error:
        print(error.as_str())
    else:
        print(tokens)