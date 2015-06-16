# -*- coding: utf-8 -*-

"""turingmarkov - Turing machine and markov algorithm emulator."""

from .markov import Algorithm
import sys, pytest, os

VERSION = "0.1.2" # Don't forget fix in setup.py

def main():
    """Execute, when user call turingmarkov."""
    if len(sys.argv) > 1 and sys.argv[1:3] == ["compile", "markov"]:
        input_file = open(sys.argv[3]) if len(sys.argv) > 3 else sys.stdin
        algo = Algorithm(input_file.readlines())
        input_file.close()
        print(algo.compile())
    elif len(sys.argv) == 2 and sys.argv[1] == "test":
        path = os.path.abspath(os.path.dirname(__file__))
        sys.argv[1] = path
        pytest.main()
    elif len(sys.argv) == 2 and sys.argv[1] == "version":
        print("TuringMarkov", VERSION)
    else:
        print('Usage: {name} command [file]'.format(name=sys.argv[0]))
        print('Available commands:')
        print('  compile markov : make python code from markov stdin->stdout')
        print('  test           : run internal tests')
        print('  version        : print version and exit')

if __name__ == "__main__":
    main()
