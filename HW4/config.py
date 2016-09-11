GRAPH_PATH = '/Users/admin/Documents/CS6200/HW4/wt2g_inlinks.txt'
CRAWL_GRAPH_PATH = '/Users/admin/Documents/CS6200/HW4/graph'
RESULTS_PATH = '/Users/admin/Documents/CS6200/HW4/Results'
MAPPINGS_PATH = '/Users/admin/Documents/CS6200/HW4/'
ES_HOST = {"host": "localhost", "port": 9200}
WT2G_INDEX = 'wt2g_graph'
WT2G_TYPE  = 'wt2g_nodes'
INDEX 	= 'web_graph'
TYPE 	= 'nodes'

# Contains the encoded URLs of the pages in the Crawl Index
PAGES_PATH = '/Users/admin/Documents/CS6200/HW4/pages'
# INDEX VALUES FOR INLINKS AND OUTLINKS IN THE TUPLE
OUTLINK_INDEX = 0
INLINK_INDEX  = 1

PR_RESULT_WINDOW = 500

# SOURCE INDEX FOR HITS 
CRAWL_INDEX = '1512_great_mordenist_artist'
CRAWL_INDEX_TYPE = 'document'

# QUERY TO GET THE ROOTSET FROM ES
ROOT_SET_QUERY = '''
{
  "size": 1000,
  "query": {
    "query_string": {
      "default_field": "TEXT", 
      "query": "Great Modernist Artists"
    }
  }
}
'''

WT2G_GRAPH = {
    "settings": {
        "index": {
            "store": {
                "type": "default"
            },
            "number_of_shards": 3,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "wt2g_nodes": {
            "properties": {
                "inlinks": {
                    "type": "string",
                    "store": "true",
                },
                "outlinks": {
                    "type": "string",
                    "store": "true",
                }
            }
        }
    },
    "analysis": {
        "analyzer": {
            "my_keyword": {
                "type": "keyword",
                "filter": "lowercase"
            }
        }
    }
}