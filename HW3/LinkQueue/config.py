INDEX = 'frontier'
TYPE  = 'queue'

search_body = """
{
  "query": {
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
          "VISITED": false
        }
      }
    }
  }
}"""
