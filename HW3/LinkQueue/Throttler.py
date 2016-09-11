from HW3.config import elastic_host
from elasticsearch import Elasticsearch
from config import INDEX, TYPE, search_body
from threading import Lock
from QueueRetriever import QueueRetriever
from Queuer import Queuer
import sys
es = Elasticsearch([elastic_host], timeout=50, max_retries=10, retry_on_timeout=True)

class Throttler(object):


	def __init__(self):
		self._lock = Lock()


	def throttle(self):
		with self._lock:		
			res = es.count(index = 'frontier', doc_type = 'queue', body=search_body)
			print res['count']
			if res['count'] > 5000:
				print "Keeping the queue short!"
				all_links = es.search(index = INDEX, doc_type = TYPE, size = 100000, body=search_body)
								
				if len(all_links['hits']) > 0:					
					q = all_links['hits']['hits']					
					throttle_docs = q[5000:]					
					ret = QueueRetriever()
					ret.update(throttle_docs)
					print "Queue length throttled!"


# t = Throttler()
# t.throttle()