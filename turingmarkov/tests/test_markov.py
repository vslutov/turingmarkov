# -*- coding: utf-8 -*-

"""Test case for markov algorithm emulator."""

from turingmarkov.markov import Algorithm
from pytest import raises

def test_algorithm_init():
    """Test if we can create empty algorithm and algorithm with rules."""
    algo = Algorithm()
    assert algo.rules == []
    algo = Algorithm(['aa -> a', 'bb -> b', 'cc -> c'])
    assert algo.rules == [('aa', 'a', 0), ('bb', 'b', 0), ('cc', 'c', 0)]

class TestAlgorithm:

    """Test case for methods: add_rule, execute, execute_once."""

    algo = None

    def setup(self):
        """Setup before each test."""
        self.algo = Algorithm()
        assert self.algo.rules == []

    def test_algorithm_add_rule(self):
        """There are sample of right and wrong rules."""
        self.algo.add_rule('aa -> a')
        assert len(self.algo.rules) == 1
        assert self.algo.rules[-1] == ('aa', 'a', 0)

        self.algo.add_rule('b c c cc -> c')
        assert len(self.algo.rules) == 2
        assert self.algo.rules[-1] == ('bcccc', 'c', 0)

        self.algo.add_rule('c b b bb => c')
        assert len(self.algo.rules) == 3
        assert self.algo.rules[-1] == ('cbbbb', 'c', 1)

        with raises(SyntaxError):
            self.algo.add_rule('b - > c')
        with raises(SyntaxError):
            self.algo.add_rule('b = > c')
        with raises(SyntaxError):
            self.algo.add_rule('b -> c -> d')
        with raises(SyntaxError):
            self.algo.add_rule('b => c => d')
        with raises(SyntaxError):
            self.algo.add_rule('b -> c => d')
        with raises(SyntaxError):
            self.algo.add_rule('b => c -> d')

        self.algo.add_rule('  bb  =>  b  ')
        assert len(self.algo.rules) == 4
        assert self.algo.rules[-1] == ('bb', 'b', 1)

    def test_algorithm_execute(self):
        """Test `alpha -> alpha alpha` and remove double letters."""
        self.algo.add_rule('#x -> xx#')
        self.algo.add_rule('#  => ') # Terminal rule
        self.algo.add_rule('   -> #')

        string = 'xxx'
        string = self.algo.execute(string, max_tacts=500)
        assert string == 'xxxxxx'
        assert self.algo.last_rule == ('#', '', 1)

        self.algo = Algorithm(['aa -> a', 'bb -> b', 'cc -> c'])

        string = 'abbbaacc'
        string = self.algo.execute(string, max_tacts=500)
        assert string == 'abac'
        assert self.algo.last_rule is None

        self.algo = Algorithm(['x -> xx']) # Forever algo
        with raises(TimeoutError):
            self.algo.execute('xxx', max_tacts=500)


    def test_algorithm_execute_once(self):
        """Test `alpha -> alpha alpha` and remove double letters."""
        self.algo.add_rule('#x -> xx#')
        self.algo.add_rule('#  => ')
        self.algo.add_rule('   -> #')

        string = 'xxx'
        string = self.algo.execute_once(string)
        assert string == '#xxx'
        assert self.algo.last_rule == ('', '#', 0)
        string = self.algo.execute_once(string)
        assert string == 'xx#xx'
        assert self.algo.last_rule == ('#x', 'xx#', 0)
        string = self.algo.execute_once(string)
        assert string == 'xxxx#x'
        assert self.algo.last_rule == ('#x', 'xx#', 0)
        string = self.algo.execute_once(string)
        assert string == 'xxxxxx#'
        assert self.algo.last_rule == ('#x', 'xx#', 0)
        string = self.algo.execute_once(string)
        assert string == 'xxxxxx'
        assert self.algo.last_rule == ('#', '', 1)

        self.algo = Algorithm(['aa -> a', 'bb -> b', 'cc -> c'])

        string = 'abbbaacc'
        string = self.algo.execute_once(string)
        assert string == 'abbbacc'
        assert self.algo.last_rule == ('aa', 'a', 0)
        string = self.algo.execute_once(string)
        assert string == 'abbacc'
        assert self.algo.last_rule == ('bb', 'b', 0)
        string = self.algo.execute_once(string)
        assert string == 'abacc'
        assert self.algo.last_rule == ('bb', 'b', 0)
        string = self.algo.execute_once(string)
        assert string == 'abac'
        assert self.algo.last_rule == ('cc', 'c', 0)
        string = self.algo.execute_once(string)
        assert string == 'abac'
        assert self.algo.last_rule is None

    def test_algorithm_debug(self):
        """Not implemented."""
        self.algo.debug()

    def test_algorithm_compile(self):
        """Return string with code."""
        self.algo.add_rule('#x -> xx#')
        self.algo.add_rule('#  => ')
        self.algo.add_rule('   -> #')

        algo = self.algo.compile()
        assert isinstance(algo, str)
        assert "# -*- coding: utf-8 -*-" in algo
        assert "from turingmarkov.markov import Algorithm" in algo

        assert "'#x->xx#'" in algo
        assert "'#=>'" in algo
        assert "'->#'" in algo

    def test_algorithm_quoting(self):
        r"""' should transform to \' in compiled code."""
        self.algo = Algorithm(["'x->xx'", "'=>", "->'"])
        algo = self.algo.compile()
        assert isinstance(algo, str)
        assert "\"'x->xx'\"" in algo
        assert "\"'=>\"" in algo
        assert "\"->'\"" in algo
