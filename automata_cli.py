import sys
import json
from statemachine import Step, StateMachine, PlainTextParser, SyntexException



def print_usage():
    print "python statemachine.py [filename] [strings]"


def savecsv(string, steps, result, filepath, append):

    if append:
        f = open(filepath, "a")
    else:
        f = open(filepath, "w")

    f.write("Test String:, %s \n" % (string,))
    for step in steps:
        f.write("%s,%s,%s \n" %
                (step.init_state, step.symbol, step.final_state))
    f.write("Result:, %s \n" % (str(result),))


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

    content = input_file.read()

    parser = PlainTextParser()

    try:
        machine = parser.parse(content)
    except SyntexException, e:
        print e
        return None

    return machine


def test(tests, machine):

    total = len(tests)
    failed = 0

    print "#####################################################"
    for (test, expected) in tests:
        print "Test String: " + test + " Expected Result: " + str(expected)
        (result, steps) = machine.evaluate(test)
        print_step_list(steps)
        print "Result: " + str(result)
        if result == expected:
            print " TEST PASS! "
        else:
            print " TEST FAILED! "
            failed += 1

    print "#####################################################"
    print str((total - failed)) + "/" + str(total) + " Tests Passed"


def print_machine_description(name, start, success, transitions, extended=False):
    print "#####################################################"
    print " MACHINE:         %s " % (str(name),)
    print " START STATE:     %s " % (str(start),)
    print " ACCEPTOR STATES: %s " % (str(success),)
    print " TRANSITIONS:     %s " % (str(transitions),)
    if extended:
        pass
    print "#####################################################"


def print_results(string, steps, result, final_state):
    if result:
        accept = " Yes!"
    else:
        accept = " No!"

    print "#####################################################"
    print " Test String:    %s " % (string,)
    for (index, step) in enumerate(steps):
        print "    %d %s" % (index, str(step))
    print " Final State:    %s " % (str(final_state),)
    print " Accept?:        %s " % (str(accept),)
    print "#####################################################"


def main(argv):

    if len(argv) > 1:

        filepath = argv[0]

        #print "Description File: %s" % (filepath)

        #tests = [("aaa", False), ("accc", True)]

        machine = parse_text_file(filepath)

        if machine is None:
            print "Process Terminated: Could not parse autonama file"
            return

        print_machine_description(
            filepath, machine.start, machine.success, machine.transitions)

        for string in argv[1:]:
            (result, final_state, steps) = machine.evaluate(string)
            print_results(string, steps, result, final_state)
            savecsv(string, steps, result, "testfile.csv", True)
        #test(tests, machine)

        # dump_machine(machine)

    else:
        print_usage()

if __name__ == "__main__":
    main(sys.argv[1:])
