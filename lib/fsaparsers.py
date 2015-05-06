from statemachine import FSADescription

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
    TYPE_CUNT = "CUNT"

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
        self._reset_state()

        self.rules = {}

        tokens = []
        valid_types = self.parser_dict.keys()

        lines = string.splitlines()
        for (line_number, line) in enumerate(lines):
            line.lstrip()  # remove leading white space

            # tokenize line and determain type
            strings = line.split(' ', 1)

            type_string = strings[0].upper()

            # case where there is only one token in the line
            if len(strings) == 1:
                content_string = ""
            else:
                content_string = (strings[1].replace(" ", ""))

            # print "Parsing: %s" % (line,)
            # print "(%s,%s)" % (type_string, content_string)

            if (type_string in valid_types):
                tokens.append((type_string, content_string))
            else:
                # If unknown line type, raise exception and return None.
                raise SyntexException(line_number, line)
                return None

        # Convert token list to data structures
        for (token_type, content_string) in tokens:
            self.parser_dict[str(token_type)](str(content_string))

        description = FSADescription(self.start, self.success, self.rules)

        return description
