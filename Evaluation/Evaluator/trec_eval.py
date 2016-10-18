from Measures import *
from Reader import ResultsReader
from Qrel import Qrel
from os.path import join
from config import *
import sys
import matplotlib.pyplot as plt


# path for the result file for queries assigned to the team
result_file = join(RESULTS_PATH, 'results')


def interpolated_precision(precision, rank):
    prec_from_r = []
    for val, prec in precision.iteritems():
        if val >= rank:
            prec_from_r.append(prec)
    return max(prec_from_r)


def plot_pr_curve(precision, recall):

    x_coords = []
    y_coords = []
    for val in precision:
        x_coords.append(recall[val])
        # ip = interpolated_precision(precision, val)
        y_coords.append(precision[val])

    plt.scatter(x_coords, y_coords)
    plt.plot(x_coords, y_coords)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    filename = "{}-NIP.png".format(qID)
    plot_file_path = join(PLOT_PATH, filename)
    print plot_file_path
    plt.draw()
    plt.savefig(plot_file_path)
    plt.close()


def build_results(prec, recall, f1, ndcg, rp, ap, meta):
    data = {}
    for i in k:
        prec_key = "prec_{}".format(i)
        rec_key = "rec_{}".format(i)
        f1_key = "f1_{}".format(i)
        ndcg_key = "ndcg_{}".format(i)
        data[prec_key] = prec.get(i, 0.0)
        data[rec_key] = recall.get(i, 0.0)
        data[f1_key] = f1.get(i, 0.0)
    data['ID'] = qID
    data['avg_prec'] = ap
    data['ndcg'] = ndcg
    data['rp'] = rp
    data['ID'] = meta['ID']
    data['R'] = meta['R']
    data['rel_ret'] = meta['rr']
    print OUTPUT.format(**data)


def docs_with_grades(docs, qrel, qID):
    values = qrel.values
    tuples = []
    for doc in docs:
        tuples.append((doc, values[qID].get(doc, 0)))
    return tuples


if __name__ == '__main__':
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        if len(sys.argv) == 4:
            qrel_index = 2
            trec_index = 3
        else:
            qrel_index = 1
            trec_index = 2

        qrel_file = sys.argv[qrel_index]
        trec_file = sys.argv[trec_index]
        reader = ResultsReader()
        results = reader.read(trec_file)
        qrel = Qrel(qrel_file)
        ndcg_qrel = Qrel(qrel_file)
        prec_results = {}
        recall_results = {}
        f1_results = {}
        rp = {}
        avg_precision = {}
        ndcg = {}
        total_R = 0
        total_rr = 0

        for qID, res in results.iteritems():
            prec_results[qID], recall_results[qID] = pr_plot(res, qrel, qID)
            f1_results[qID] = F_Measure_k(prec_results[qID], recall_results[qID])
            rp[qID] = R_Precision(prec_results[qID], qrel, qID)
            avg_precision[qID] = average_precision(res, qrel, qID, prec_results[qID])
            ndcg[qID] = nDCG(docs_with_grades(res, ndcg_qrel, qID))
            R = qrel.total_rel(qID)
            rr = qrel.ret_rel(qID, res)
            total_R += R
            total_rr += rr
            meta = {
                'ID': qID,
                'R': R,
                'rr': rr
            }
            if sys.argv[1] == '-q':
                build_results(prec_results[qID], recall_results[qID], f1_results[qID], ndcg[qID], rp[qID], avg_precision[qID], meta)

        # calculate averages over all the queries
        prec_avgs = {}
        recall_avgs = {}
        f1_avgs = {}
        ndcg_avg = 0
        for val in k:
            prec_avgs[val] = 0
            recall_avgs[val] = 0
            f1_avgs[val] = 0
            for qID, prec in prec_results.iteritems():
                prec_avgs[val] += prec.get(val, 0.0)
                recall_avgs[val] += recall_results[qID].get(val, 0.0)
                f1_avgs[val] += f1_results[qID].get(val, 0.0)
            prec_avgs[val] /= len(results)
            recall_avgs[val] /= len(results)
            f1_avgs[val] /= len(results)

        ndcg_sum = 0
        for qID in ndcg:
            ndcg_sum += ndcg[qID]

        ndcg_avg = ndcg_sum / len(ndcg)
        rp = sum(rp[qID] for qID in rp) / len(rp)
        avg_precision = sum(avg_precision[qID] for qID in avg_precision) / len(avg_precision)
        meta = {
                'ID': len(results),
                'R': total_R,
                'rr': total_rr
            }


        build_results(prec_avgs, recall_avgs, f1_avgs, ndcg_avg, rp, avg_precision, meta)
        # store PR Curves for all queries

        for qID in results:
            print recall_results[qID][1000]
            plot_pr_curve(prec_results[qID], recall_results[qID])

    else:
        print "Usage: trec_eval [-q] <qrel_file> <trec_file>"
