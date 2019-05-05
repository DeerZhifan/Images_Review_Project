# -*- coding: utf-8 -*-
import sys


class Hello:
    """测试"""
    def __init__(self, string1, string2):
        self.string1 = string1
        self.string2 = string2

    def engine(self):
        return self.string1 + self.string2


if __name__ == "__main__":
    a = []
    for i in range(1, len(sys.argv)):
        a.append((sys.argv[i]))
    hello = Hello("hello ", "world")
    print(hello.engine())
