from elasticsearch import Elasticsearch
from config import *
from os.path import join
from django.utils.encoding import iri_to_uri
import sys

es = Elasticsearch()

queries = {
    '151201': 'picasso paintings',
    '151202': 'brancusi sculptures',
    '151203': 'barcelona gaudi architecture'
}

def get_results(query):
    """
    :param query: Query to be used for search in ES
    :return: a list containing IDs of all the results for the given query
    """
    body = SEARCH_BODY.format(query)
    res = es.search(index=INDEX, doc_type=TYPE, body=body, size=RESULT_SIZE)
    IDs = []
    for hit in res['hits']['hits']:
        IDs.append((hit['_id'], hit['_score']))

    return IDs


def write_results(qID, results):
    """
    :param qID: Query ID
    :param results: a list containing search results for the given Query ID
    :return: Void
    :effect: Write the results to file in trec format
             <qID> Q0 <docID> <rank> <score> <exp>
    """
    print "Writing results to file"
    string = ''
    rank = 1
    for docID, score in results:
        docID = iri_to_uri(docID)
        string += "{} {} {} {} {} {}\n".format(qID, "Q0", docID, rank, score, "exp")
        rank += 1

    file_path = join(RESULTS_PATH, 'results')
    with open(file_path, 'a') as f:
        f.write(string)

    print "Done Writing!"


if __name__ == "__main__":

    for queryID, query in queries.iteritems():
        results = get_results(query)
        write_results(queryID, results)
