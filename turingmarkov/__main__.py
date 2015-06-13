# -*- coding: utf-8 -*-

from .markov import Algorithm
import sys

def main():
    if len(sys.argv) == 2 and sys.argv[1] == '--compile-markov':
        algo = Algorithm(sys.stdin.readlines())
        print(algo.compile())
    else:
        print('Usage: {name} command'.format(name=sys.argv[0]))
        print('Available commands:')
        print('  --compile-markov : make python code from markov stdin->stdout')

if __name__ == "__main__":
    main()
