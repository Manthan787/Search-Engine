from __future__ import division
from config import k
import math


def dcg_at_k(k, results, ideal=False):
    dcg = 0
    if ideal:
        results = sorted(results, key=lambda tup: tup[1], reverse=True)
    dcg += results[0][1]
    for i in range(1, k):
        try:
            dcg += results[i][1] / math.log(i + 1, 2)
        except:
            dcg += 0

    return dcg


def nDCG_at_k(k, results):
    return dcg_at_k(1000, results) / dcg_at_k(1000, results, ideal=True)


def nDCG(results):
    ndcg_results = {}
    return nDCG_at_k(1000, results)


def F_Measure_k(precisions, recalls):
    f_results = {}

    for limit in k:
        if limit in precisions:
            precision = precisions[limit]
            recall = recalls[limit]
            f_results[limit] = F_Measure(precision, recall)
        else:
            f_results[limit] = 0.0

    return f_results


def F_Measure(p, r):
    try:
        return (2*p*r) / (p + r)
    except:
        return 0.0


def R_Precision(precisions, qrel, qID):
    R = qrel.total_rel(qID)
    return precisions[R]


def precision_k(results, qrel, qID):
    precision_results = {}
    for limit in k:
        ret_rel = qrel.ret_rel(qID, results[:limit])
        precision_results[limit] = precision(ret_rel, limit)
        # precision_results.setdefault(qID, {}).setdefault(limit, )

    return precision_results


def average_precision(results, qrel, qID, precisions):
    sum_precision = 0
    R = qrel.total_rel(qID)
    k = 0
    for docID in results:
        k += 1
        if qrel.isRelevant(qID, docID):
            sum_precision += precisions[k]

    return sum_precision / R


def precision_at(k, results, qrel, qID):
    ret_rel = qrel.ret_rel(qID, results[:k])
    prec = precision(ret_rel, k)
    return prec


def recall_at(k, results, qrel, qID):
    R = 0
    for res in results:
        if qrel.isRelevant(qID, res):
            R += 1
    ret_rel = qrel.ret_rel(qID, results[:k])
    return recall(ret_rel, R)


def precision(ret_rel, N):
    """
    :param ret_rel: No of retrieved documents that were relevant
    :param N: No of relevant documents in total
    :return: precision
    """
    # print "Precision at %s" %N
    # print "RETREL %s" %ret_rel
    return ret_rel / N



def recall_k(results, qrel, qID):
    total_relevant = qrel.total_rel(qID)
    recall_results = {}
    for limit in k:
        ret_rel = qrel.ret_rel(qID, results[:limit])
        recall_results[limit] = recall(ret_rel, total_relevant)
        # recall_results.setdefault(qID, {}).setdefault(limit, recall(ret_rel, total_relevant))

    return recall_results


def recall(ret_rel, relevant):
    return ret_rel / relevant


def precision_at_test(k, results, qrel, qID):
    ret_rel = 0
    for res in results[:k]:
        if qrel[res] > 0:
            ret_rel += 1

    prec = precision(ret_rel, k)
    return prec


def pr_plot(results, qrel, qID):
    prec = {}
    recall = {}
    for i in range(1, len(results)+1):
        prec[i] = precision_at(i, results, qrel, qID)
        recall[i] = recall_at(i, results, qrel, qID)
    return prec, recall


def test():
    results = [1, 2, 3, 4, 5]
    qrel = {1: 1, 2: 0, 3:0, 4:1, 5:0}

    print precision_at_test(5, results, qrel, "1")

    results = [(1, 3), (2, 2), (3, 3), (4, 0), (5, 1), (6, 2)]
    print nDCG_at_k(6, results)

    print nDCG(results, [1, 2, 6])


if __name__ == '__main__':
    test()
