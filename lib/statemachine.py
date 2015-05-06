class StateMachine(object):

    """ 
        StateMachine object simulates a FSA 

        start - begining state
        success - list of acceptor states
        transitions - dictionary { s1 : [(symb, s2)] }  
    """

    def __init__(self, description):
        #self.start = start
        #self.success = success
        #self.transitions = transitions
        self.fsa = description
        self.state = self.fsa.start
        self.step_count = 0
        self.steps = []
        #self.states = self._find_states()
        #self.terminal_states = self._find_terminal_states()

    def _step(self, symbol):

        init_state = self.state

        possible_states = self.fsa.transitions.get(str(self.state), None)

        if possible_states is not None:
            for (transition, next_state) in possible_states:
                if symbol == transition:
                    self.state = next_state
                    break

        self.step_count += 1

        return Step(init_state, symbol, self.state)

    def evaluate(self, string):
        ''' simulates the machine for the input string, returns Tuple (accept, [steps])

            accept - is a boolean, true if the input string is accepted, false otherwise
            [steps] - list of step objects, representing machine state changes while excuting the string.
        '''
        self.steps = []
        self.step_count = 0
        self.state = self.fsa.start

        for symbol in list(string):
            step_result = self._step(symbol)
            self.steps.append(step_result)

        if self.state in self.fsa.success:
            return (True, self.state, self.steps)
        else:
            return (False, self.state, self.steps)


class FSADescription(object):

    def __init__(self, start, success, transitions):
        self.start = start
        self.success = success
        self.transitions = transitions
        self.states = self._find_states()
        self.terminal_states = self._find_terminal_states()

    def _find_states(self):
        states = set([])
        states.add(self.start)
        for state in self.success:
            states.add(state)

        for (key, trans) in self.transitions.iteritems():
            states.add(key)

            for (symbol, next_state) in trans:
                states.add(next_state)

        return states

    def _find_terminal_states(self):
        terminal_states = set([])
        for state in self.states:
            if self.transitions.get(state, None) is None:
                terminal_states.add(state)

        return terminal_states

    def __str__(self):
        return "FSADescription: {start=%s, success=%s, transitions=%s}" % (self.start, self.success, self.transitions)

class Step(object):

    ''' 
        Step object represents one FSM state transition

        init_state  - state before input symbol
        symbol      - input symbol
        final_state - state after transition
    '''

    def __init__(self, init_state, symbol, final_state):
        self.init_state = init_state
        self.symbol = symbol
        self.final_state = final_state

    def __str__(self):
        return "< %s : %s -> %s >" % (self.init_state, self.symbol, self.final_state)
