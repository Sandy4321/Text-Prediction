import heapq

class internal_node(object):
	def __init__(self,character):
		self.character = character
		self.children = []
		self.counter = 1
		self.children_map = {}

	def add_child(self,child):
		if type(child) is internal_node:
			self.children_map[child.character] = child
			heapq.heappush(self.children,(-1*child.counter,child))

	def is_leaf(self):
		return len(self.children) == 0

	def get_child(self,char):

		if char not in self.children_map:
			return None
		else:
			return self.children_map[char]

	def get_greater_child(self):

		return self.children[0][1]


	def next_word(self):
		current = self
		word = ""
		while True:
			if current.is_leaf() is True: 
				break
			word = word + current.character
			current = current.get_greater_child()
			if current.character == " ":
				break

		return word + current.character



	def __repr__(self):
		return str(self.character)

class vocabulary:
	
	def __init__(self):
		self.root = internal_node(' ')

	def add_string(self,string):
		current = self.root
		idx = 0
		while idx < len(string):
			the_child = current.get_child(string[idx])
			
			if the_child is None:
				new_node = internal_node(string[idx])
				current.add_child(new_node)
				current = new_node

			else:
				the_child.counter = the_child.counter + 1
				current = the_child
			
			idx += 1

	def bfs(self):
		q = [self.root]
		visit = set()
		visit.add(self.root)
		while len(q) > 0:
			c = q.pop()

			for ch in c.children:
				if ch not in visit:
					visit.add(ch[1])
					q.append(ch[1])

	def predict_next_word(self,string):
		idx = 0
		current = self.root
		while idx < len(string):
			the_node = current.get_child(string[idx])
			if the_node is None:
				return []
			else:
				current = the_node

			idx = idx + 1

		if current.is_leaf() is True:
			return []

		if current.character != " ":
			current = current.get_greater_child()
		
		words = []
		for child in current.children:
			if current.character == " ":
				words.append( child[1].next_word() )
			else:
				words.append( current.character + child[1].next_word() )

		return words



'''

data = vocabulary()
data.add_string("que es eso")
data.add_string("que es perra")
data.add_string("que es locura")
data.add_string("que es JOJO")
data.add_string("que garra eso")
data.add_string("que gonorrea eso")
data.bfs()
print data.predict_next_word("eso")
'''