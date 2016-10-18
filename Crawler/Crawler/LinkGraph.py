from HW3.config import elastic_host
from elasticsearch import Elasticsearch, helpers
import uuid
from threading import Lock
es = Elasticsearch([elastic_host])
INDEX = 'links'
TYPE  = 'map'

class LinkGraph(object):

	''' Creates a LinkGraph object
		Args:
			links: a dictionary with a url as a key and its outlinks as value 
	'''
	def __init__(self):
		self.inlinks 	= {}
		self.outlinks 	= {}
		self._lock		= Lock()		


	def update(self, links):
		with self._lock:
			for url, outlinks in links.iteritems():
				self.__updateOutlinks(url, outlinks)
				self.__updateInlinks(url, outlinks)
	

	def __updateOutlinks(self, url, outlinks):
		if url in self.outlinks:
			self.outlinks[url] = self.outlinks[url] + outlinks
		else:
			self.outlinks[url] = outlinks


	def __updateInlinks(self, url, outlinks):
		for link in outlinks:
			self.inlinks.setdefault(link, []).append(url)


	def inlinkcount(self, url):
		return len(self.inlinks.get(url, []))


	def outlinkcount(self, url):
		return len(self.outlinks.get(url, []))


	def empty(self):
		return len(self.inlinks) == 0 and len(self.outlinks) == 0


	def store(self):
		with self._lock:
			print "Storing links!"
			gen = self.__action()
			helpers.bulk(es, gen)			
			self.outlinks = {}

	def __action(self):
		for link, outlinks in self.outlinks.iteritems():
			for l in outlinks:
				id = link + "#" + l				
				yield({'_index': INDEX, '_type': TYPE, '_id': id,'body':{'SRC_LINKS': link, 'DEST_LINKS': l}})


if __name__ == "__main__":
	links = {'h': ['a', 'b', 'c', 'd'], 'a': ['c', 'd']}
	graph = LinkGraph()
	graph.update(links)
	links = {'h': ['f'], 'f': ['a', 'b', 'c']}
	graph.update(links)
	print graph.inlinks
	print graph.outlinks
