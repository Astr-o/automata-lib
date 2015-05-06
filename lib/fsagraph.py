class FSAGraph(object):

    def __init__(self, fsa_description):
        self.description = fsa_description
        self.nodes = self._create_nodes()

        print str(self)

    def _create_nodes(self):
        nodes = {}
        for (my_id, state) in enumerate(self.description.states):
            state_transitions = self.description.transitions.get(state)
            if state_transitions is None:
                node_transitions = None
            else:
                node_transitions = {}
                for (symbol, neighbour_name) in state_transitions:
                    node_transitions[symbol] = neighbour_name

            nodes[state] = Node(my_id, state, node_transitions)

        for node in nodes.values():
            node._set_graph(nodes)

        return nodes

    def accept_visitor(self, visitor):
        self.nodes.get(self.description.start).accept_visitor(visitor)
        return visitor

    def __str__(self):
        return "FSAGraph: {description=%s \n, nodes=%s \n}" % (self.description, self.nodes)


class Visitor(object):

    def __init__(self):
        self.count = 0
        self.visited = set([])

    def _visit(self, node):
        self._report_begin(node)
        if node in self.visited:
            result = False
        else:
            self.count += 1
            result = True
        self._report_end(node)
        return result

    def _report_begin(self, node):
        print "Visitor %s entering  node=%s, node_id=%s, count=%d" % (type(self), node.name, node.id, self.count)
        print  node.neighbours
    def _report_end(self, node):
        print "Visitor %s exiting  node=%s, node_id=%s, count=%d" % (type(self), node.name, node.id, self.count)


class Node(object):

    def __init__(self, my_id, name, my_transitions, active=False):
        self.id = my_id
        self.active = active
        self.name = name
        self.transitions = my_transitions
        if self.transitions is not None:
            self.neighbours = set(self.transitions.values())
        else:
            self.neighbours = set([])

    def _set_graph(self, graph):
        self.graph = graph

    def accept_visitor(self, visitor):
        if visitor._visit(self) and self.neighbours is not []:
            for neighbour in self.neighbours:
                self.graph[neighbour].accept_visitor(visitor)

        return visitor
