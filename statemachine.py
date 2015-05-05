class SyntexException(Exception):

    def __init__(self, message, line_number, line):
        super(Exception, self).__init__(message)
        self.line_number = line_number
        self.line = line

'''
Format

START "s"
SUCCESS "q, r, tt"
RULES
# S1 : Symb : S2 
ENDRULES
'''


class PlainTextParser(object):

    type_start = "START"
    type_success = "SUCCESS"
    type_begin_rules = "RULES"
    type_rule = "#"
    type_end_rules = "ENDRULES"

    TOP_LEVEL = 0
    IN_RULES = 1

    def __init__(self):
        self.parser_state = PlainTextParser.TOP_LEVEL

        self.parser_dict = {
            PlainTextParser.type_start:         self._parse_start,
            PlainTextParser.type_success:       self._parse_success,
            PlainTextParser.type_begin_rules:   self._parse_begin_rules,
            PlainTextParser.type_rule:          self._parse_rule,
            PlainTextParser.type_end_rules:     self._parse_end_rules,
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

    def parse(self, string):

        self.rules = {}

        tokens = []

        lines = string.splitlines()
        for (line_number, line) in enumerate(lines):
            line.lstrip()  # remove leading white space

            # tokenize line and determain tupe
            strings = line.split(' ', 1)

            type_string = strings[0].upper()
            if len(strings) == 1:
                content_string = ""
            else:
                content_string = (strings[1].replace(" ", ""))

            print "Parsing: %s" % (line,)
            print "(%s,%s)" % (type_string, content_string)

            if (type_string in self.parser_dict.keys()):
                tokens.append((type_string, content_string))
            else:
                # If unknown line type, raise exception and return None.
                message = "Syntex Error: unknown line type \n  (%d) - %s \n" % (
                    line_number, line)

                raise SyntexException(message, line_number, line)
                return None

        for (token_type, content_string) in tokens:
            self.parser_dict[str(token_type)](str(content_string))

        return StateMachine(self.start, self.success, self.rules)


class StateMachine(object):

    def __init__(self, start, success, transitions):
        self.start = start
        self.success = success
        self.transitions = transitions
        self.state = start
        self.step_count = 0
        self.states = self.find_states()

    def find_states(self):
        states = set([])
        states.add(self.start)
        for state in self.success:
            states.add(state)

        for (key, trans) in self.transitions.iteritems():
            states.add(key)

            for (symbol, next_state) in trans:
                states.add(next_state)

        return states

    def step(self, symbol):

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
