# -*- coding: utf-8 -*-

"""Emulator of turing machine."""

TEMPLATE = """#!/bin/env python3
# -*- coding: utf-8 -*-
from turingmarkov.turing import Machine
from sys import stdin
"""


class Machine:

    """Turing Machine emulator.

    Read the doc: https://github.com/cmc-python/turingmarkov

    Example 1: Add letter a after word.
    >>> x = Machine(['a', 'b', 'c', '_'])
    >>> x.add_state('0 ,R, ,R, ,R, ,R, a,N,!')
    >>> x.execute('abacab')
    abacaba
    """

    START_STATE = '0'
    TERM_STATE = '!'
    EMPTY_SYMBOL = '_'

    def __init__(self, alphabet):
        """See help(type(x))."""
        self.states = dict()
        self.state = None
        self.tape = None
        self.head = None

        if self.EMPTY_SYMBOL in alphabet:
            self.alphabet = alphabet
        else:
            raise SyntaxError('Missed "_" symbol in alphabet')

    def _add_rule(self, state, rule):
        """Parse rule and add it to machine (for internal use)."""
        if rule.strip() == "-":
            parsed_rule = None
        else:
            parsed_rule = rule.split(',')

            if  (len(parsed_rule) != 3 or
                 parsed_rule[1] not in ['L', 'N', 'R'] or
                 len(parsed_rule[2]) > 1):
                raise SyntaxError('Wrong format of rule: ' + rule)

            if parsed_rule[0] == "":
                parsed_rule[0] = self.alphabet[len(self.states[state])]
            if parsed_rule[2] == "":
                parsed_rule[2] = state

        self.states[state].append(parsed_rule)

    def add_state(self, string):
        """Add state and rules to machine."""
        parsed_string = string.split()
        if len(parsed_string) > 0:
            state, rules = parsed_string[0], parsed_string[1:]

            if len(rules) != len(self.alphabet):
                raise SyntaxError('Wrong count of rules ({cur}/{exp}): {string}'
                                  .format(cur=len(rules), exp=len(self.alphabet),
                                          string=string))

            if state in self.states or state == self.TERM_STATE:
                raise SyntaxError('Double definition of state: ' + state)
            else:
                self.states[state] = []

            for rule in rules:
                try:
                    self._add_rule(state, rule)
                except SyntaxError as err:
                    self.states.pop(state)
                    raise err

    def check(self):
        """Check semantic rules."""
        has_term = False

        if self.START_STATE not in self.states:
            raise SyntaxError('Undefined start rule')

        for state in self.states:
            for rule in self.states[state]:
                if rule is not None:
                    if rule[2] == self.TERM_STATE:
                        has_term = True
                    elif rule[2] not in self.states:
                        raise SyntaxError('Unexpected state: ' + rule[2])

        if not has_term:
            raise SyntaxError('Missed terminate state')

    def init_tape(self, string):
        """Init system values."""
        for char in string:
            if char not in self.alphabet and not char.isspace() and char != self.EMPTY_SYMBOL:
                raise RuntimeError('Invalid symbol: "' + char + '"')

        self.check()
        self.state = self.START_STATE
        self.head = 0

        self.tape = {}
        for i in range(len(string)):
            symbol = string[i] if not string[i].isspace() else self.EMPTY_SYMBOL
            self.tape[i] = symbol

    def get_tape(self):
        """Get content of tape."""
        result = ''
        for i in range(min(self.tape), max(self.tape) + 1):
            symbol = self.tape[i] if self.tape[i] != self.EMPTY_SYMBOL else ' '
            result += symbol
        # Remove unnecessary empty symbols on tape
        return result.strip()

    def execute_once(self):
        """One step of execution."""
        symbol = self.tape.get(self.head, self.EMPTY_SYMBOL)

        index = self.alphabet.index(symbol)
        rule = self.states[self.state][index]

        if rule is None:
            raise RuntimeError('Unexpected symbol: ' + symbol)

        self.tape[self.head] = rule[0]

        if rule[1] == 'L':
            self.head -= 1
        elif rule[1] == 'R':
            self.head += 1

        self.state = rule[2]

    def execute(self, string, max_tacts=None):
        """Execute algorithm (if max_times = None, there can be forever loop)."""
        self.init_tape(string)
        counter = 0

        while True:
            self.execute_once()
            if self.state == self.TERM_STATE:
                break
            counter += 1
            if max_tacts is not None and counter >= max_tacts:
                raise TimeoutError("algorithm hasn't been stopped")

        return self.get_tape()

    def compile(self):
        """Return python code for create and execute machine."""
        result = TEMPLATE
        result += 'machine = Machine(' + repr(self.alphabet) + ')\n'

        for state in self.states:
            repr_state = state[0]
            for rule in self.states[state]:
                repr_state += ' ' + (','.join(rule) if rule is not None else '-')

            result += ("machine.add_state({repr_state})\n".format(repr_state=repr(repr_state)))

        result += "for line in stdin:\n"
        result += "    print(machine.execute(line))"
        return result

def build_machine(lines):
    """Build machine from list of lines."""
    if lines == []:
        raise SyntaxError('Empty file')
    else:
        machine = Machine(lines[0].split())
        for line in lines[1:]:
            if line.strip() != '':
                machine.add_state(line)
    machine.check()
    return machine
