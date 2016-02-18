import sys

class State:
	"""A state is just a collection of variable bindings."""
	def __init__(self, name):		
		self.__name__ = name	
		
	def print_state(self, state,indent=4):
		"""Print each variable in state, indented by indent spaces."""
		if state != False:
			for (name,val) in vars(state).items():
				if name != '__name__':
					for x in range(indent): sys.stdout.write(' ')
					sys.stdout.write(state.__name__ + '.' + name)
					print(' =', val)
		else:
			print('False')