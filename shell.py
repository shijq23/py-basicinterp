#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import basiclang.basic

if __name__ == '__main__':
    while True:
        text = input("basic > ")
        ast, error = basiclang.basic.run('<stdin>', text)

        if error:
            print(error.as_str())
        else:
            print(ast)