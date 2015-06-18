# -*- coding: utf-8 -*-

"""Emulator of markov algothm."""

TEMPLATE = """#!/bin/env python3
# -*- coding: utf-8 -*-
from turingmarkov.markov import Algorithm
from sys import stdin
algo = Algorithm()
"""

class Algorithm:

    """Now supports only execution of algorithm.

    >>> algo = Algorithm(['aa -> a', 'bb -> b', 'cc -> c'])
    >>> algo.execute('aabbbcb')
    abcb

    In future, there will be debug.
    """

    def __init__(self, rules=tuple()):
        """See help(type(a))."""
        self.rules = []
        self.last_rule = None

        for rule in rules:
            rule = rule.strip()
            if rule != '':
                self.add_rule(rule)

    def add_rule(self, rule):
        """Supported rules: `a -> b` and `a => b` (terminal rule)."""
        parsed_rule = None

        if rule.count('->') == 1 and rule.count('=>') == 0:
            parsed_rule = tuple(''.join(part.split()) for part in rule.split('->')) + (0,)
        elif rule.count('->') == 0 and rule.count('=>') == 1:
            parsed_rule = tuple(''.join(part.split()) for part in rule.split('=>')) + (1,)

        if parsed_rule is None:
            raise SyntaxError('Wrong format: ' + rule)
        else:
            self.rules.append(parsed_rule)

    def debug(self):
        """Now it do nothing."""
        pass

    def execute_once(self, string):
        """Execute only one rule."""
        for rule in self.rules:
            if rule[0] in string:
                pos = string.find(rule[0])
                self.last_rule = rule
                return string[:pos] + rule[1] + string[pos+len(rule[0]):]
        self.last_rule = None
        return string

    def execute(self, string, max_tacts=None):
        """Execute algorithm (if max_times = None, there can be forever loop)."""
        counter = 0
        self.last_rule = None

        while True:
            string = self.execute_once(string)
            if self.last_rule is None or self.last_rule[2]:
                break
            counter += 1
            if max_tacts is not None and counter >= max_tacts:
                raise TimeoutError("algorithm hasn't been stopped")

        return string

    def compile(self):
        """Return python code for create and execute algo."""
        result = TEMPLATE

        for rule in self.rules:
            if rule[2]:
                arrow = '=>'
            else:
                arrow = '->'
            repr_rule = repr(rule[0] + arrow + rule[1])

            result += "algo.add_rule({repr_rule})\n".format(repr_rule=repr_rule)

        result += "for line in stdin:\n"
        result += "    print(algo.execute(''.join(line.split())))"
        return result
