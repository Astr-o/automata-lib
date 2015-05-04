import sys
import json


def show_usage():
    print "python statemachine.py [filename]"


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

    if len(argv) == 1:
        print "Description File " + argv[0]

        tests = [("aaa", False), ("accc", True)]

        parsed = parse_text_file(argv[0])

        if not parsed:
            print "Process Terminated: Could not parse autonama file"
            return

        machine = StateMachine(
            parsed["start"], parsed["success"], parsed["terminal"], parsed["transitions"])

        test(tests, machine)

    else:
        show_usage()


def test(tests, machine):

    total = len(tests)
    failed = 0

    for (test, expected) in tests:
        print "Test String: " + test + " Expected Result: " + str(expected)
        result = machine.evaluate(test)
        print "Result: " + str(result)
        if result == expected:
            print " TEST PASS! "
        else:
            print " TEST FAILED! "
            failed += 1

    print "#####################################################"
    print str((total - failed)) + "/" + str(total) + " Tests Passed"


class StateMachine(object):

    def __init__(self, start, success, terminal, transitions):
        self.start = start
        self.success = success
        self.terminal = terminal
        self.transitions = transitions
        self.state = start
        self.step_count = 0

    def step(self, symbol):
        self.step_count += 1

        possible_states = self.transitions[str(self.state)]

        for (transition, next_state) in possible_states:
            if symbol == transition:
                self.state = next_state
                break

        return self.state

    def evaluate(self, string):

        self.step_count = 0

        for char in list(string):
            self.step(char)

            print "T" + str(self.step_count) + " Transition Character: " + str(char) + "  New State: " + str(self.state)

        if self.state in self.success:
            print "State: " + str(self.state) + " is successful."
            return True
        else:
            print "State: " + str(self.state) + " is not successful"
            return False


if __name__ == "__main__":
    main(sys.argv[1:])
