# -*- coding: utf-8 -*-

"""Test case for cli part of turingmarkov package."""

from turingmarkov.__main__ import main, VERSION, USAGE
from pytest import raises

def test_compile_markov(tmpdir):
    """Result should be python code."""
    input_path = tmpdir.join('double.markov')
    input_path.write('#x -> xx#\n# =>\n-> #\n')
    output_path = tmpdir.join('double.py')

    with open(str(output_path), 'w') as stdout:
        main(['turingpython', 'compile', 'markov', str(input_path)], None, stdout)

    algo = output_path.read()
    assert "# -*- coding: utf-8 -*-" in algo
    assert "from turingmarkov.markov import Algorithm" in algo
    assert "'#x->xx#'" in algo
    assert "'#=>'" in algo
    assert "'->#'" in algo

    with open(str(input_path)) as stdin:
        with open(str(output_path), 'w') as stdout:
            main(['turingpython', 'compile', 'markov'], stdin, stdout)

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
