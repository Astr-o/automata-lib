class FSAGraph(object):
	def __init__(self, fsa_description):
		self.description = fsa_description
		self.nodes = self._create_nodes()

	def _create_nodes(self):
		nodes = {}
		for (my_id, state) in enumerate(self.description.states):
			state_transitions = self.description.transitions.get(state, None)
			if state_transitions is None:
				node_transitions = None
			else:
				node_transitions = {}
				for (symbol, neighbour) in state_transitions:
					node_transitions.add(symbol, neighbour)

			nodes[state] = Node(my_id, state, node_transitions)



class Visitor(object):

	def __init__(self):
		self.count = 0
		visited = set([])

	def visit(self, node):
		visited.add(node)
		self.count += 1




class Node(object):
	def __init__(self, my_id, name, my_transitions):
		self.id = my_id
		self.name = name
		self.transitions = my_transitions
		if self.transitions is None:
			self.neighbours = []
		else:
			self.neighbours = self.transitions.values()
	
	def accept_visitor(self,visitor):
		visitor.visit(self)
		for neighbour in neighbours:
			neighbour.accept_visitor(visitor)



