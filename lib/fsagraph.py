"""
    FSAGraph is implemented using object nodes, with relations represented by
    a dictornary in each node mapping symbols to neighbour nodes. 

    The FSAGraph implements a Breadth First Traversal visitor in its current form.

    To implement visitors extend Visitor() and override the on_visit method.
"""


class FSAGraph(object):

    """ This object models the FSA as a graph for analysis
        and GUI rendering
    """

    def __init__(self, fsa_description):
        self.description = fsa_description
        self.nodes = self._create_nodes()

        # print str(self)

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
        self.nodes.get(self.description.start)._accept_visitor(visitor)
        return visitor

    def __str__(self):
        return "FSAGraph: {description=%s \n, nodes=%s \n}" % (self.description, self.nodes)


class Visitor(object):

    ''' Base visitor class

        override the method on_visit(self,node) in a subclass to create a custom
        visitor see CounterVisitor for an example

        report_begin and report_end are called at the begining and end of a 
        visit respectively if report is True for the visitor.
    '''

    # Graph traversal types
    DFS_TRAVERSE = 0
    BFS_TRAVERSE = 1

    def __init__(self, report=False):
        self.count = 0
        self.visited = set([])
        self.report = report

    def _visit(self, node):
        if self.report:
            self.report_begin(node)

        if node in self.visited:
            result = False
        else:
            result = True
            self.visited.add(node)
            self.on_visit(node)

        if self.report:
            self.report_end(node)
        return result

    def on_visit(self, node):
        pass

    def report_begin(self, node):
        print "Visitor %s entering  node=%s, node_id=%s" % (type(self), node.name, node.id)
        print "Neighbours %s " % (str(node.neighbours),)

    def report_end(self, node):
        print "Visitor %s exiting  node=%s, node_id=%s" % (type(self), node.name, node.id)


class CounterVisitor(Visitor):

    def __init__(self, report=False):
        Visitor.__init__(self, report)
        self.count = 0

    def on_visit(self, node):
        self.count += 1
        print str(self.count)


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

    def _accept_visitor(self, visitor, traversal=Visitor.BFS_TRAVERSE):
        if visitor._visit(self) and self.neighbours is not []:
            for neighbour in self.neighbours:
                self.graph[neighbour]._accept_visitor(visitor)

        return visitor
