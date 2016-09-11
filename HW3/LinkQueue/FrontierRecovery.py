from HW3.config import elastic_host
from elasticsearch import Elasticsearch, helpers
from QueueRetriever import QueueRetriever
from config import INDEX, TYPE

def action(links):
	for link in links:
		source = link['_source']
		yield ({'_op_type': 'update', 
				'_index': INDEX,
				'_type': TYPE,
				'_id': link['_id'],
				'refresh': True,				
				'doc': {'VISITED': False}
				})


if __name__ == "__main__":
	es = Elasticsearch([elastic_host], timeout=500, max_retries=2, retry_on_timeout=True)
	res = es.search(index=INDEX, doc_type=TYPE, 
					body='''
					{"query": {
							    "filtered": {
							      "query": {
							        "function_score": {
							          "functions": [
							            {
							              "script_score": {
							                "script_id": "MAGIC_DEQUEUE",
							                "lang": "groovy"
							              }
							            }
							          ],
							          "boost_mode": "replace"
							        }
							      },
							      "filter": {
							        "term": {
							          "DISCOVERY_WAVE_NO": 5
							        }
							      }
							    }
							  }}''', size=10000)

	helpers.bulk(es, action(res['hits']['hits'][5000:6000]))


