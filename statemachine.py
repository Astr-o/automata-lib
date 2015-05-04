import sys
import json


def show_usage():
    print "python statemachine.py [filename] [strings]"


def dump_machine(machine):
    print(json.dumps(machine.state))
    print(json.dumps(machine.success))
    print(json.dumps(machine.terminal))
    print(json.dumps(machine.transitions))


def parse_text_file(filepath):
    try:
        input_file = open(filepath, 'r')
    except IOError, e:
        print "IOError while opening file: " + filepath
        print e
        return None

    line = input_file.readline()

    line_types = ["start", "success", "terminal", "transitions"]
    parsed = {}
    line_count = 0

    while line:
        line_count += 1

        line.strip()
        tokens = line.split(" ", 1)
        line_type = tokens[0]
        line_json = tokens[1]

        line_type.lower()

        if line_type in line_types:
            parsed[line_type] = json.loads(line_json)
        else:
            print "Unknown line: " + str(line_count) + "  " + line.replace('\n', ' ')
            return None

        line = input_file.readline()

    return parsed


def main(argv):

    if len(argv) > 1:
        print "Description File: %s" % (argv[0])

        #tests = [("aaa", False), ("accc", True)]

        parsed = parse_text_file(argv[0])

        if not parsed:
            print "Process Terminated: Could not parse autonama file"
            return

        machine = StateMachine(
            parsed["start"], parsed["success"], parsed["terminal"], parsed["transitions"])

        for string in argv[1:]:
            (result, steps) = machine.evaluate(string)
            print_results(string, steps, result)
        #test(tests, machine)

        # dump_machine(machine)

    else:
        show_usage()


def test(tests, machine):

    total = len(tests)
    failed = 0

    print "#####################################################"
    for (test, expected) in tests:
        print "Test String: " + test + " Expected Result: " + str(expected)
        (result, steps) = machine.evaluate(test)
        Step.print_step_list(steps)
        print "Result: " + str(result)
        if result == expected:
            print " TEST PASS! "
        else:
            print " TEST FAILED! "
            failed += 1

    print "#####################################################"
    print str((total - failed)) + "/" + str(total) + " Tests Passed"


def print_results(string, steps, result):
    print "#####################################################"
    print "Test String: %s " % (string,)
    Step.print_step_list(steps)
    print "Result: %s" % (str(result),)
    print "#####################################################"


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

    @staticmethod
    def print_step_list(steps):
        line = 1
        for step in steps:
            print "%d) %s" % (line, str(step))
            line += 1

    def __init__(self, init_state, symbol, final_state):
        self.init_state = init_state
        self.symbol = symbol
        self.final_state = final_state

    def __str__(self):
        return "< %s : %s -> %s >" % (self.init_state, self.symbol, self.final_state)

if __name__ == "__main__":
    main(sys.argv[1:])
