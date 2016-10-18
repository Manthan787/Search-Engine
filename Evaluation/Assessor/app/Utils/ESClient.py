from elasticsearch import Elasticsearch
from ..config import *

class ESClient(object):

    es = Elasticsearch([ES_HOST])

    def search(self, query):
        SEARCH_BODY = self.__getSearchBody(query)
        result = self.es.search(index = INDEX, doc_type = TYPE, body = SEARCH_BODY, size = RESULT_SIZE)
        return result['hits']['hits']


    def __getSearchBody(self, query):
        body = '''
            {{
              "query": {{
                "query_string": {{
                  "default_field": "TEXT",
                  "query": "{}"
                }}
              }}
            }}
        '''.format(query)

        return body