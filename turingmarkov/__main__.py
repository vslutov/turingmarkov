# -*- coding: utf-8 -*-

"""turingmarkov - Turing machine and markov algorithm emulator."""

from .markov import Algorithm
import pytest, os, sys

VERSION = "0.1.3" # Don't forget fix in setup.py

USAGE = '''Usage: turingmarkov command [file]
Available commands:
    compile markov : make python code from markov algorithm and put to stdout
    compile turing : make python code from turing machine and put to stdout
    run markov     : run markov algorithm (from requred file); stdin->stdout
    run turing     : run turing machine (from requred file); stdin->stdout
    test           : run internal tests
    version        : print version and exit
    help           : print this help and exit'''

def main(argv, stdin, stdout):
    """Execute, when user call turingmarkov."""
    if len(argv) > 1 and argv[1:3] == ["compile", "markov"]:
        input_file = open(argv[3]) if len(argv) > 3 else stdin
        algo = Algorithm(input_file.readlines())
        input_file.close()
        print(algo.compile(), file=stdout)
    elif len(argv) == 4 and argv[1:3] == ["run", "markov"]:
        with open(argv[3]) as input_file:
            algo = Algorithm(input_file.readlines())
        for line in stdin:
            print(algo.execute(''.join(line.split())), file=stdout)
    elif len(argv) == 2 and argv[1] == "test":
        path = os.path.abspath(os.path.dirname(__file__))
        argv[1] = path
        pytest.main()
    elif len(argv) == 2 and argv[1] == "version":
        print("TuringMarkov", VERSION, file=stdout)
    else:
        print(USAGE, file=stdout)
        if not (len(argv) == 2 and argv[1] == "help"):
            exit(1)

def exec_main():
    """Hook for testability."""
    main(sys.argv, sys.stdin, sys.stdout)

if __name__ == "__main__":
    exec_main()
