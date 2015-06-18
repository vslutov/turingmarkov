# -*- coding: utf-8 -*-

"""Test case for cli part of turingmarkov package."""

from turingmarkov.__main__ import main, load_markov, load_turing, VERSION, USAGE
from pytest import raises

def test_load_markov(tmpdir):
    """Result should be Markov Algorithm."""
    input_path = tmpdir.join('double.markov')
    input_path.write('#x -> xx#\n\n# =>\n\n-> #\n')

    markov = load_markov(['turingmarkov', 'run', 'markov', str(input_path)], None)
    assert markov.rules == [('#x', 'xx#', 0), ('#', '', 1), ('', '#', 0)]

    with open(str(input_path)) as stdin:
        markov = load_markov(['turingmarkov', 'compile', 'markov'], stdin)
    assert markov.rules == [('#x', 'xx#', 0), ('#', '', 1), ('', '#', 0)]

def test_load_turing(tmpdir):
    """Result should be Turing Machine."""
    input_path = tmpdir.join('double.markov')
    input_path.write('a b c _\n\n0 - ,R, ,R, a,N,!\n')
    machine = load_turing(['turingmarkov', 'run', 'turing', str(input_path)], None)
    assert machine.alphabet == ['a', 'b', 'c', '_']
    assert machine.states['0'] == [None,
                                   ['b', 'R', '0'],
                                   ['c', 'R', '0'],
                                   ['a', 'N', '!']]

def test_compile_turing(tmpdir):
    """Result should be python code."""
    input_path = tmpdir.join('append.turing')
    input_path.write('a b c _\n\n0 ,R, ,R, ,R, a,N,!\n')
    output_path = tmpdir.join('append.py')

    with open(str(output_path), 'w') as stdout:
        main(['turingmarkov', 'compile', 'turing', str(input_path)], None, stdout)

    machine = output_path.read()
    assert "# -*- coding: utf-8 -*-" in machine
    assert "from turingmarkov.turing import Machine\n" in machine
    assert "machine = Machine(['a', 'b', 'c', '_'])\n" in machine
    assert "machine.add_state('0 a,R,0 b,R,0 c,R,0 a,N,!')\n" in machine

    with open(str(input_path)) as stdin:
        with open(str(output_path), 'w') as stdout:
            main(['turingmarkov', 'compile', 'turing'], stdin, stdout)

    machine = output_path.read()
    assert "# -*- coding: utf-8 -*-" in machine
    assert "from turingmarkov.turing import Machine\n" in machine
    assert "machine = Machine(['a', 'b', 'c', '_'])\n" in machine
    assert "machine.add_state('0 a,R,0 b,R,0 c,R,0 a,N,!')\n" in machine

def test_run_turing(tmpdir):
    """Easy double word test."""
    machine_path = tmpdir.join('append.turing')
    machine_path.write('a b c _\n\n0 ,R, ,R, ,R, a,N,!\n')
    input_path = tmpdir.join('input.txt')
    input_path.write('abacab\n')
    output_path = tmpdir.join('output.txt')

    with open(str(input_path)) as stdin:
        with open(str(output_path), 'w') as stdout:
            main(['turingmarkov', 'run', 'turing', str(machine_path)], stdin, stdout)

    assert output_path.read() == 'abacaba\n'

def test_compile_markov(tmpdir):
    """Result should be python code."""
    input_path = tmpdir.join('double.markov')
    input_path.write('#x -> xx#\n# =>\n-> #\n')
    output_path = tmpdir.join('double.py')

    with open(str(output_path), 'w') as stdout:
        main(['turingmarkov', 'compile', 'markov', str(input_path)], None, stdout)

    algo = output_path.read()
    assert "# -*- coding: utf-8 -*-" in algo
    assert "from turingmarkov.markov import Algorithm" in algo
    assert "'#x->xx#'" in algo
    assert "'#=>'" in algo
    assert "'->#'" in algo

    with open(str(input_path)) as stdin:
        with open(str(output_path), 'w') as stdout:
            main(['turingmarkov', 'compile', 'markov'], stdin, stdout)

    algo = output_path.read()
    assert "# -*- coding: utf-8 -*-" in algo
    assert "from turingmarkov.markov import Algorithm" in algo
    assert "'#x->xx#'" in algo
    assert "'#=>'" in algo
    assert "'->#'" in algo

def test_run_markov(tmpdir):
    """Easy double word test."""
    algo_path = tmpdir.join('double.markov')
    algo_path.write('#x -> xx#\n# =>\n-> #\n')
    input_path = tmpdir.join('input.txt')
    input_path.write('xxx')
    output_path = tmpdir.join('output.txt')

    with open(str(input_path)) as stdin:
        with open(str(output_path), 'w') as stdout:
            main(['turingmarkov', 'run', 'markov', str(algo_path)], stdin, stdout)

    assert output_path.read() == 'xxxxxx\n'

def test_version(tmpdir):
    """Test that it's print current version."""
    output_path = tmpdir.join('output.txt')

    with open(str(output_path), 'w') as stdout:
        main(['turingmarkov', 'version'], None, stdout)

    assert output_path.read() == 'TuringMarkov ' + VERSION + '\n'

def test_usage(tmpdir):
    """Test that it's print usage (with exit code 1)."""
    output_path = tmpdir.join('output.txt')

    with open(str(output_path), 'w') as stdout:
        main(['turingmarkov', 'help'], None, stdout)
    assert output_path.read() == USAGE + '\n'

    with open(str(output_path), 'w') as stdout:
        with raises(SystemExit):
            main(['turingmarkov', 'wrong_command'], None, stdout)
    assert output_path.read() == USAGE + '\n'
