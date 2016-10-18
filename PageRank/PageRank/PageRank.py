from __future__ import division
import math
from HW4.config import OUTLINK_INDEX, INLINK_INDEX, PR_RESULT_WINDOW


class PageRank( object ):

	# Damping / Teleportation Factor
	d 	= 0.85	
	prev_perplexities = []

	def __init__(self, graph):
		self.PR 	= dict()
		self.graph  = graph		


	def run(self):
		# get sinknodes, nodes with no outlinks
		sinkNodes 	= self.__getSinkNodes()
		print "Sinknodes: %s" %(len(sinkNodes))
		N = len(self.graph)
		for page in self.graph:
			self.PR[page] = 1 / N

		iteration = 0
		while not self.__hasConverged():
			iteration += 1
			print "Iteration %s" %iteration
			newPR = {}
			sinkPR = 0
			for page in sinkNodes:
				sinkPR += self.PR[page]

			for page in self.graph:
				newPR[page] =  (1 - PageRank.d) / N
				newPR[page] +=  PageRank.d * (sinkPR / N)
				links = self.graph.get(page)
				for inlink in links[INLINK_INDEX]:
					outlink_count = self.__getOutlinkCount(inlink)
					newPR[page] += (PageRank.d * self.PR.get(inlink)) / outlink_count

			for page in self.graph:
				self.PR[page] = newPR[page]

		return self.PR


	def __getSinkNodes(self):
		print "Getting sink nodes..."	
		nodes = []
		for node in self.graph:
			links = self.graph.get(node)
			if len(links[OUTLINK_INDEX]) == 0:
				nodes.append(node)
		return nodes


	def __hasConverged(self):
		entropy = 0
		for page, PR in self.PR.iteritems():
			entropy += PR * math.log(PR, 2)			

		perplexity = pow(2, -entropy)
		print "Perplexity : %s" %perplexity
		self.__storePerplexity(perplexity)
		if len(self.prev_perplexities) < 4:
			return False

		first = self.prev_perplexities[0]		
		for p in self.prev_perplexities[1:]:
			diff = abs(first - p)
			print "Difference: %s" %diff			
			if not diff <= 1:
				return False

		return True


	def __storePerplexity(self, perplexity):
		if len(self.prev_perplexities) == 4:
			del self.prev_perplexities[0]

		self.prev_perplexities.append(perplexity)			


	def __getOutlinkCount(self, link):
		return len(self.graph[link][OUTLINK_INDEX])