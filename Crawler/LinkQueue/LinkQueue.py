class Queue(object):

	def __init__(self, links):		
		self.links  = links		
		self.ptr    = 0
		self.visited = []


	def next(self):
		next_url = self.links[self.ptr]
		ptr = self.ptr
		self.ptr += 1
		return next_url, ptr


	def get(self, noOfElems):
		elems = {}
		while len(elems) != noOfElems:
			url, ptr = self.next()
			elems[url['_id']] = (url['_source']['PARENT_SCORE'], ptr)							

			if len(self.links) < self.ptr + 1:
				break

		return elems


	def find(self, ptr):		
		return self.links[ptr]

	
	def update(self, ptr, values):
		el = self.find(ptr)
		for key, value in values.iteritems():
			el['_source'][key] = value

		self.visited.append(ptr)


	def empty(self):
		print "visited len: %s, links len : %s" %(len(self.visited), len(self.links))
		return len(self.visited) == len(self.links)


	def visit(self, ptr):
		self.visited.append(ptr)


	def length(self):
		return len(self.links)
