from elasticsearch import Elasticsearch
from HW4.config import *
from Mapper import Mapper
from django.utils.encoding import iri_to_uri
import sys
import traceback


class ESClient(object):
    es = Elasticsearch([ES_HOST], timeout=120)

    def getGraph(self):
        try:
            page = self.es.search(index=INDEX,
                                  doc_type=TYPE, scroll='1m', size=10000,
                                  body='''{
								  	"query": {
								  		"match_all": {}
								  	}
								  }''')
            sid = page['_scroll_id']
            scrollSize = page['hits']['total']
            # Links from ES converted to a dict
            pages = {}
            size = 0
            all_hits = []
            while scrollSize > 0:
                hits = page['hits']['hits']
                scrollSize = len(hits)
                size += scrollSize
                all_hits += hits
                sys.stdout.write("scrolled through %d Docs... \r" % size)
                sys.stdout.flush()
                for hit in hits:
                    ID = hit['_id']
                    outlinks = hit['_source']['outlinks']
                    inlinks = hit['_source']['inlinks']
                    pages[ID] = [outlinks, inlinks]

                sid = page['_scroll_id']
                page = self.es.scroll(scroll_id=sid, scroll='2m')
            return pages
        except Exception as e:
            print "Error while fetching links from ES"
            traceback.print_exc()


    def getRootSet(self, mapper=None):
        try:
            print CRAWL_INDEX
            result = self.es.search(index=CRAWL_INDEX, doc_type=CRAWL_INDEX_TYPE, body=ROOT_SET_QUERY)
            documents = result['hits']['hits']
            root_set = []
            for document in documents:
                url = document['_id']
                if mapper is not None:
                    try:
                        urlID = mapper.lookup(url)
                        root_set.append(urlID)
                    except ValueError:
                        pass
                else:
                    root_set.append(url)

            return root_set

        except Exception as e:
            print "%s exception: %s" % (type(e), e)


    def getCrawledPages(self, mapper):
        try:
            print "Getting crawled pages"
            page = self.es.search(index=CRAWL_INDEX,
                                  doc_type=CRAWL_INDEX_TYPE,
                                  scroll='2m', size=10000, fields=['_id'])
            sid = page['_scroll_id']
            scrollSize = page['hits']['total']
            pages = []
            size = 0

            while scrollSize > 0:
                hits = page['hits']['hits']
                for hit in hits:
                    print hit['_id']
                    pages.append(mapper.lookup(hit['_id']))
                scrollSize = len(hits)
                size += scrollSize
                sys.stdout.write("scrolled through %s links..." % (size))
                sys.stdout.flush()
                sid = page['_scroll_id']
                page = self.es.scroll(scroll_id=sid, scroll='2m')

            return pages

        except Exception as e:
            print "Error while fetching links from ES"
            traceback.print_exc()


	def createWT2GGraph(self):
		self.es.create(index=WT2G_INDEX, doc_type=WT2G_TYPE)
    def __transform(self, hits):
        ''' Converts elasticsearch hits format to a dict
			with the format: 
			{
				'id': (outlinks, inlinks)
			}
		'''

        transformed_hits = {}
        for hit in hits:
            ID = hit['_id']
            outlinks = hit['_source']['outlinks']
            inlinks = hit['_source']['inlinks']

            transformed_hits[ID] = (outlinks, inlinks)

        return transformed_hits

    def __merge_dicts(self, dict1, dict2):
        merged = dict1.copy()
        merged.update(dict2)
        return merged


if __name__ == '__main__':
    client = ESClient()
    mapper = Mapper.fromFile('link_map')
    pages = client.getCrawledPages(mapper)
    print "Writing to file"
    with open('/Users/admin/Documents/CS6200/HW4/pages', 'w') as f:
        for page in pages:
            f.write(page + '\n')
    print "DONE!"
