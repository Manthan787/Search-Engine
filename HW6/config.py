QID = 0
ASSESSOR = 1
DOCID = 2
GRADE = 3

# INDEX = "ap_dataset"
INDEX = "1512_great_mordenist_artist"
TYPE  = "document"


AP_QREL_FILE = '/Users/admin/Documents/CS6200/AP_DATA/qrels.adhoc.51-100.AP89.txt'
# QUERIES_FILE = '/Users/admin/Documents/CS6200/AP_DATA/queries.short.txt'
QUERIES_FILE = '/Users/admin/Documents/CS6200/HW6/queries'
FEATURES_PATH = '/Users/admin/Documents/CS6200/HW6/'
RESULTS_PATH = "/Users/admin/Documents/CS6200/HW6/Result"

TREC_EVAL_PATH = "/Users/admin/Documents/CS6200/HW1/trec_eval"
QREL_PATH = "/Users/admin/Documents/CS6200/AP_DATA/qrels.adhoc.51-100.AP89.txt"
# QREL_PATH = "/Users/admin/Documents/CS6200/HW5/Evaluator/qrels.new.txt"

BODY = '''
        {{
          "query": {{
            "match": {{
              "_id": "{docno}"
            }}
          }},
          "script_fields": {{
            "tf": {{
              "script": {{
                "inline": "_index[field][term].tf()",
                "params": {{
                  "field": "{field}",
                  "term": "{term}"
                }}
              }}
            }},
            "df": {{
              "script": {{
                "inline": "_index[field][term].df()",
                "params": {{
                  "field": "{field}",
                  "term": "{term}"
                }}
              }}
            }},
            "ttf": {{
              "script": {{
                "inline": "_index[field][term].ttf()",
                "params": {{
                  "field": "{field}",
                  "term": "{term}"
                }}
              }}
            }}
          }}
        }}'''