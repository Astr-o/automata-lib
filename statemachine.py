

class SyntexException(Exception):

    ''' raised when parser finds unexpected syntex in string '''

    def __init__(self, line_number, line):
        message = "Syntex Error: unknown line type in input string \n    line %d - %s \n" % (
            line_number, line)
        super(Exception, self).__init__(message)
        self.line_number = line_number
        self.line = line


class PlainTextParser(object):

    ''' 
        Parser object for plain text format

        single method .parse(string) accepts a FSM description as a plain text string
        and returns a StateMachine object.  

        Format Example (requires new line characters)

        START "s"
        SUCCESS "q, r, tt"
        RULES
        # S1 : Symb : S2 
        ENDRULES

    '''

    # Type tags
    TYPE_START = "START"
    TYPE_SUCCESS = "SUCCESS"
    TYPE_BEGIN_RULES = "RULES"
    TYPE_RULE = "#"
    TYPE_END_RULES = "ENDRULES"

    # Parser States
    TOP_LEVEL = 0
    IN_RULES = 1

    def __init__(self):
        self.parser_state = PlainTextParser.TOP_LEVEL

        # Parser type handler functions
        self.parser_dict = {
            PlainTextParser.TYPE_START:         self._parse_start,
            PlainTextParser.TYPE_SUCCESS:       self._parse_success,
            PlainTextParser.TYPE_BEGIN_RULES:   self._parse_begin_rules,
            PlainTextParser.TYPE_RULE:          self._parse_rule,
            PlainTextParser.TYPE_END_RULES:     self._parse_end_rules,
        }

    def _parse_start(self, string):
        self.start = string

    def _parse_success(self, string):
        self.success = string.split(",")

    def _parse_begin_rules(self, string):
        self.parser_state = PlainTextParser.IN_RULES

    def _parse_rule(self, string):
        (init_state, symbol, final_state) = string.split(":")
        temp_rules = self.rules.get(init_state, None)
        if temp_rules is None:
            self.rules[init_state] = [(symbol, final_state)]
        else:
            self.rules[init_state].append((symbol, final_state))

    def _parse_end_rules(self, string):
        self.parser_state = PlainTextParser.TOP_LEVEL

    def _reset_state(self):
        self.state = PlainTextParser.TOP_LEVEL
        self.start = None
        self.success = None
        self.rules = None

    def parse(self, string):

        self.rules = {}

        tokens = []

        lines = string.splitlines()
        for (line_number, line) in enumerate(lines):
            line.lstrip()  # remove leading white space

            # tokenize line and determain type
            strings = line.split(' ', 1)

            type_string = strings[0].upper()

            if len(strings) == 1:
                content_string = ""
            else:
                content_string = (strings[1].replace(" ", ""))

            # print "Parsing: %s" % (line,)
            # print "(%s,%s)" % (type_string, content_string)

            if (type_string in self.parser_dict.keys()):
                tokens.append((type_string, content_string))
            else:
                # If unknown line type, raise exception and return None.
                raise SyntexException(line_number, line)
                return None

        # Convert token list to data structures
        for (token_type, content_string) in tokens:
            self.parser_dict[str(token_type)](str(content_string))

        return StateMachine(self.start, self.success, self.rules)


class StateMachine(object):

    """ 
        StateMachine object simulates a FSA 

        start - begining state
        success - list of acceptor states
        transitions - dictionary { s1 : [(symb, s2)] }  
    """

    def __init__(self, start, success, transitions):
        self.start = start
        self.success = success
        self.transitions = transitions
        self.state = start
        self.step_count = 0
        self.steps = []
        self.states = self._find_states()

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

    def _step(self, symbol):

        init_state = self.state

        possible_states = self.transitions.get(str(self.state), None)

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
        self.state = self.start

        for symbol in list(string):
            step_result = self._step(symbol)
            self.steps.append(step_result)

        if self.state in self.success:
            return (True, self.state, self.steps)
        else:
            return (False, self.state, self.steps)


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
