# -*- coding: utf-8 -*-

from .markov import Algorithm
import sys

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '--compile-markov':
        ALGO = Algorithm(sys.stdin.readlines())
        print(ALGO.compile())
    else:
        print('Usage: {name} command'.format(name=sys.argv[0]))
        print('Available commands:')
        print('  --compile-markov : make python code from markov stdin->stdout')
