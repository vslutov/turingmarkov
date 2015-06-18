# -*- coding: utf-8 -*-

"""Test case for turing machine emulator."""

from turingmarkov.turing import Machine, build_machine, TEMPLATE
from pytest import raises

def test_init():
    """Test, that machine is possible to create."""
    machine = Machine(['a', 'b', 'c', '_'])
    assert machine.alphabet == ['a', 'b', 'c', '_']
    assert machine.head is None
    assert machine.state is None
    assert machine.tape is None

class TestMachine:

    """Test case for Machine class."""

    machine = None
    def setup(self):
        """Setup machine (can be overloaded in tests."""
        self.machine = Machine(['a', 'b', 'c', '_'])

    def test_machine_add_state(self):
        """Test syntax."""
        self.machine.add_state('0  ,R,  ,R,  ,R,  a,N,1')

        assert self.machine.states['0'] == [['a', 'R', '0'],
                                            ['b', 'R', '0'],
                                            ['c', 'R', '0'],
                                            ['a', 'N', '1']]

        self.machine.add_state('1  ,L,  -  ,L,  _,R,!')

        assert self.machine.states['1'] == [['a', 'L', '1'],
                                            None,
                                            ['c', 'L', '1'],
                                            ['_', 'R', '!']]
        assert len(self.machine.states) == 2

    def test_machine_syntax(self):
        """Test syntax (and semantic) rules of machine."""
        self.machine.add_state('0  ,R,  ,R,  ,R,  a,N,!')
        self.machine.add_state('')

        with raises(SyntaxError):
            self.machine.add_state('0  ,R,  ,R,  ,R,  a,N,!') # Duplicate
        with raises(SyntaxError):
            self.machine.add_state('1  R,  ,R,  ,R,  a,N,!') # One comma
        with raises(SyntaxError):
            self.machine.add_state('2  ,,R,  ,R,  ,R,  a,N,!') # Too many comma
        with raises(SyntaxError):
            self.machine.add_state('3  ,R, ,R,  ,R,  ,R,  a,N,!') # Too many rules
        with raises(SyntaxError):
            self.machine.add_state('4  ,R,  ,,  ,R,  a,N,!') # Missed action
        with raises(SyntaxError):
            self.machine.add_state('5  ,R,  ,R,  a,N,!') # Missed rule

        assert len(self.machine.states) == 1

    def test_machine_check(self):
        """Should raise error, if something wrong."""
        with raises(SyntaxError):
            self.machine.check()
        self.machine.add_state('0  ,R,  ,R,  ,R,  a,N,!')
        self.machine.check() # without exception
        self.machine.add_state('1  ,L,  ,L,  ,L,  a,R,2')
        with raises(SyntaxError):
            self.machine.check()
        self.machine.add_state('2  ,L,  ,L,  ,L,  a,R,2')
        self.machine.check() # without exception

        with raises(SyntaxError):
            self.machine = Machine(['a'])

        self.machine = Machine(['a', '_'])
        self.machine.add_state('0 ,L, ,R,')
        with raises(SyntaxError):
            self.machine.check()

    def test_machine_init_tape(self):
        """Init head, state and tape."""
        with raises(SyntaxError):
            self.machine.init_tape('abacab')
        assert self.machine.head is None
        assert self.machine.state is None
        assert self.machine.tape is None

        self.machine.add_state('0  ,R,  ,R,  ,R,  a,N,!')
        with raises(RuntimeError):
            self.machine.init_tape('addd') # Invalid symbol
        assert self.machine.head is None
        assert self.machine.state is None
        assert self.machine.tape is None

        self.machine.init_tape('abacab')
        assert self.machine.head == 0
        assert self.machine.state == self.machine.START_STATE
        assert [self.machine.tape[i] for i in range(len(self.machine.tape))] == list('abacab')

    def test_machine_get_tape(self):
        """Get value of tape (_ and ' ' is empty symbols)."""
        self.machine.add_state('0  ,R,  ,R,  ,R,  a,N,!')
        self.machine.init_tape('   aba caba_caba  caba   ')
        assert self.machine.get_tape() == 'aba caba caba  caba'

    def test_machine_execute_once(self):
        """Test step-by-step execution."""
        self.machine.add_state('0  ,R,  ,R,  -  c,L,!')
        self.machine.init_tape('ab')
        assert self.machine.tape.get(self.machine.head, self.machine.EMPTY_SYMBOL) == 'a'
        self.machine.execute_once()
        assert self.machine.head == 1
        assert self.machine.state == '0'
        assert self.machine.tape[0] == 'a'
        assert self.machine.tape[1] == 'b'
        self.machine.execute_once()
        assert self.machine.head == 2
        assert self.machine.state == '0'
        assert self.machine.head not in self.machine.tape
        self.machine.execute_once()
        assert self.machine.head == 1
        assert self.machine.state == self.machine.TERM_STATE
        assert self.machine.tape[1] == 'b'
        assert self.machine.tape[2] == 'c'

        assert self.machine.get_tape() == 'abc'

        self.machine.init_tape('c')
        with raises(RuntimeError):
            self.machine.execute_once()

    def test_machine_execute(self):
        """Test all in one execute (and all exception)."""
        self.machine.add_state('0  ,R,  ,R,  ,R,  a,N,!')
        assert self.machine.execute('abacab', max_tacts=500) == 'abacaba'
        with raises(RuntimeError):
            self.machine.execute('daba', max_tacts=500)

        self.machine = Machine(['a', 'b', '_'])
        self.machine.add_state('0 ,R, ,N,! ,R,')
        with raises(TimeoutError):
            self.machine.execute('aaa', max_tacts=500)

        self.machine = Machine(['0', '1', '_'])
        self.machine.add_state('0 ,R, ,R, ,L,1')
        self.machine.add_state('1 1,N,! 0,L, 1,N,!')
        assert self.machine.execute('1010', max_tacts=500) == '1011'
        assert self.machine.execute('1011', max_tacts=500) == '1100'
        assert self.machine.execute('1111', max_tacts=500) == '10000'
        assert self.machine.execute('1', max_tacts=500) == '10'
        assert self.machine.execute('0', max_tacts=500) == '1'

        self.machine = Machine(['a', 'b', 'c', '_', '#'])
        self.machine.add_state('0    ,R,    ,R,   ,R,   #,L,1    -')
        self.machine.add_state('1    ,L,    ,L,   ,L,    ,R,2   ,L,')
        self.machine.add_state('2   _,R,   _,R,3 _,R,4   ,R,!  _,R,!')
        self.machine.add_state('3    ,R,    ,R,   ,R,   b,L,1   ,R,')
        self.machine.add_state('4    ,R,    ,R,   ,R,   c,L,1   ,R,')
        assert self.machine.execute('aabaaabacabc', max_tacts=500) == 'bbcbc'

    def test_machine_compile(self):
        """White box testing."""
        self.machine.add_state('0 ,R,   ,R,  ,L,1 -')
        self.machine.add_state('1 1,N,!  -  1,N,! -')

        code = self.machine.compile()
        assert isinstance(code, str)
        assert code.startswith(TEMPLATE)

        assert "machine = Machine(['a', 'b', 'c', '_'])\n" in code
        assert "machine.add_state('0 a,R,0 b,R,0 c,L,1 -')\n" in code
        assert "machine.add_state('1 1,N,! - 1,N,! -')\n" in code

def test_build_machine():
    """Input is array of strings."""
    machine = build_machine(['a b c _', '0 ,R, ,R, ,R, a,N,!'])
    assert machine.alphabet == ['a', 'b', 'c', '_']
    assert machine.states == {'0': [['a', 'R', '0'],
                                    ['b', 'R', '0'],
                                    ['c', 'R', '0'],
                                    ['a', 'N', '!']]}

    with raises(SyntaxError):
        build_machine([])
