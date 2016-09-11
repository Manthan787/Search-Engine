from HW3.config import elastic_host
from elasticsearch import Elasticsearch, helpers
from config import INDEX, TYPE
es = Elasticsearch([elastic_host], timeout=500, max_retries=2, retry_on_timeout=True)

class DocIndexer(object):

	def __init__(self, crawledDocs):
		self.crawledDocs = crawledDocs


	def index(self):
		print "Indexing Crawled Documents"
		try:
			helpers.bulk(es, self.action())
		except Exception as e:
			print "--------Error while Bulk Indexing Documents : %s" %e


	def action(self):
		for url, doc in self.crawledDocs.iteritems():
			source = doc.buildDocPayload()
			yield ({'_index': INDEX, '_type': TYPE, '_id': url, '_source': source})
