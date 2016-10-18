from HW3.config import elastic_host
from elasticsearch import Elasticsearch, helpers
from config import INDEX, TYPE, search_body
from Queue import Queue
import time

es = Elasticsearch([elastic_host], timeout=50, max_retries=10, retry_on_timeout=True)

class QueueRetriever(object):

	def retrieve(self):
		print "Retrieving"
		# es.indices.refresh(index = INDEX)

		res = es.search(index = INDEX, doc_type = TYPE, 
						size = 2000, body = search_body)

		if len(res['hits']) > 0:
			links = res['hits']['hits']
			print "Updating retrieved Records. -> VISITED: true"
			print len(links)
			self.update(links)			
			return links
		else:			
			return []			


	def update(self, links):
		action = self.__actionUpdate(links)
		res = helpers.bulk(es, action)


	def __actionUpdate(self,links):
		for link in links:
			source = link['_source']
			yield ({'_op_type': 'update', 
					'_index': INDEX,
					'_type': TYPE,
					'_id': link['_id'],
					'refresh': True,				
					'doc': {'VISITED': True}
					})

# ret = QueueRetriever()
# print ret.retrieve()
