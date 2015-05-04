class StateMachine(object):

    def __init__(self, start, success, terminal, transitions):
        self.start = start
        self.success = success
        self.terminal = terminal
        self.transitions = transitions
        self.state = start
        self.step_count = 0

    def step(self, symbol):

        init_state = self.state

        possible_states = self.transitions[str(self.state)]

        for (transition, next_state) in possible_states:
            if symbol == transition:
                self.state = next_state
                break

        self.step_count += 1

        return Step(init_state, symbol, self.state)

    def evaluate(self, string):
        self.steps = []
        self.step_count = 0
        self.state = self.start

        for symbol in list(string):
            step_result = self.step(symbol)
            self.steps.append(step_result)

        if self.state in self.success:
            return (True, self.steps)
        else:
            return (False, self.steps)


class Step(object):
    def __init__(self, init_state, symbol, final_state):
        self.init_state = init_state
        self.symbol = symbol
        self.final_state = final_state

    def __str__(self):
        return "< %s : %s -> %s >" % (self.init_state, self.symbol, self.final_state)

