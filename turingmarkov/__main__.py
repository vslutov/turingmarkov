# -*- coding: utf-8 -*-

"""turingmarkov - Turing machine and markov algorithm emulator."""

from .markov import Algorithm
import sys, pytest, os

def main():
    """Execute, when user call turingmarkov."""
    if len(sys.argv) == 2 and sys.argv[1] == 'compile-markov':
        algo = Algorithm(sys.stdin.readlines())
        print(algo.compile())
    elif len(sys.argv) == 2 and sys.argv[1] == 'test':
        path = os.path.abspath(os.path.dirname(__file__))
        sys.argv[1] = path
        pytest.main()
    else:
        print('Usage: {name} command'.format(name=sys.argv[0]))
        print('Available commands:')
        print('  compile-markov : make python code from markov stdin->stdout')
        print('  test           : run internal tests')

if __name__ == "__main__":
    main()
