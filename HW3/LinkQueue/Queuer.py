from HW3.config import elastic_host
from elasticsearch import Elasticsearch, helpers
from config import INDEX, TYPE
from threading import Lock
es = Elasticsearch([elastic_host], timeout=500)

class Queuer(object):

	def __init__(self, links):
		self.links = links
		self._lock = Lock()


	def enqueue(self):
		with self._lock:		
			print "Updating Frontier!"	
			es.indices.refresh(index = INDEX)	
			action = self.__actionUpsert()
			helpers.bulk(es, action)			


	def __actionUpsert(self):		
		for link in self.links:
			source = link['_source']
			yield ({'_op_type': 'update', 
					'_index': INDEX,
					'_type': TYPE,
					'_id': link['_id'],
					'refresh': True,				
					'script': {
							'id': 'MAGIC_ENQUEUE',
							'params': source					
						},
					"upsert": source					
					})