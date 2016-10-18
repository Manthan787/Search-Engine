from __future__ import division
from Qrel import Qrel
from elasticsearch import Elasticsearch
from ..config import *
from HW1.Query.Parser import get_queries
from HW1.Query.Processor import loadDocLengths
from HW1.Query.RetrievalModels import okapiBM25, unigramLaplace, unigramJM, tfidf, IDF
from HW2.Index.ProximitySearch import rank as proximity_score
from os.path import join
import math


functions = [okapiBM25, unigramLaplace, unigramJM, tfidf]
es = Elasticsearch()
N = 198236
FIELD = 'TEXT'

# Get scores for each document
def get_scores(qrel, queries):
    doc_scores = {}
    for qID, query in queries.iteritems():
        doc_scores[qID] = {}
        qrel_docs = qrel.get(qID, {})
        print "queryID %s" %qID
        print query
        for term in query:
            if term == '':
                continue
            print term
            docs = get_doc_properties(qrel_docs, term)
            for docID, hits in docs.iteritems():
                doc_scores[qID].setdefault(docID, {})
                doc = {}
                print docID
                fields = hits[0]['fields']
                doc['tf'] = int(fields['tf'][0])
                doc['df'] = int(fields['df'][0])
                doc['ttf'] = int(fields['ttf'][0])
                add_all_features(doc_scores[qID][docID], doc, docLength[docID])
        print "Getting proximity scores!"
        for docID in qrel_docs:
            positions, terms = get_positions(docID, query)
            score = proximity_score(positions, docLength).get(docID, 0)
            idf_sum = get_idf_sum(terms)
            doc_scores[qID].setdefault(docID, {}).setdefault('prox', score)
            doc_scores[qID].setdefault(docID, {}).setdefault('IDF_SUM', idf_sum)
    return doc_scores


def get_idf_sum(terms):
    sum = 0
    for term, values in terms.iteritems():
        df = values['doc_freq']
        try:
            sum += math.log(N / df)
        except:
            sum += 0
    return sum


def get_positions(docID, query):
    positions = {}
    for term in query:
        res = es.termvectors(index=INDEX, doc_type=TYPE, id=docID, fields=[FIELD],
                             body= '''{
                                    "term_statistics": true
                                }''')
        terms = res['term_vectors'][FIELD]['terms']
        if term not in terms:
            # positions.setdefault(docID, {}).setdefault(term, [])
            continue
        else:
            for pos in terms[term]['tokens']:
                positions.setdefault(docID, {}).setdefault(term, []).append(pos['position'])
    return positions, terms


def add_all_features(scores, doc, docLength):
    for scoring_func in functions:
        func_name = scoring_func.__name__
        if func_name in scores:
            scores[func_name] += scoring_func(doc, docLength)
        else:
            scores[func_name] = scoring_func(doc, docLength)


def get_doc_properties(IDs, term):
    docs = {}
    for ID in IDs:
        search_body = BODY.format(docno=ID, term=term, field=FIELD)
        res = es.search(index=INDEX, doc_type=TYPE, body=search_body)
        docs[ID] = res['hits']['hits']
    return docs


def write_to_file(scores, qrel, name, docLength):
    print "Writing features to file"
    string = ''
    for qID, doc_scores in scores.iteritems():
        for dID, model_scores in doc_scores.iteritems():
            string += "{} {} {} {} {} {} {} {} {} {}\n".format(
                qID,
                dID,
                model_scores['okapiBM25'],
                model_scores['unigramLaplace'],
                model_scores['unigramJM'],
                model_scores['tfidf'],
                model_scores['prox'],
                docLength[dID],
                model_scores['IDF_SUM'],
                qrel[qID][dID])

    path = join(FEATURES_PATH, name)
    with open(path, 'w') as f:
        f.write(string)


def getDocLengths(qrel):
    print "Getting Doc Lengths"
    docLength = {}
    for qID, docs in qrel.iteritems():
        for doc in docs:
            length = 0
            res = es.termvectors(index=INDEX, doc_type=TYPE, id=doc)
            terms = res['term_vectors'][FIELD]['terms']
            for term, val in terms.iteritems():
                length += val['term_freq']
            docLength[doc] = length
    return docLength


if __name__ == '__main__':
    q = Qrel(QREL_PATH)
    qrel = q.getAsDict()
    docLength = getDocLengths(qrel)
    # docLength = loadDocLengths()
    queries = get_queries(QUERIES_FILE)
    scores = get_scores(qrel, queries)
    write_to_file(scores, qrel, 'all_data', docLength)