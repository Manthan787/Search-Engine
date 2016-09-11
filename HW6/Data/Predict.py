from __future__ import division
from sklearn import linear_model
from sklearn import svm
from sklearn import tree
from sklearn import neural_network
from ..config import *
from os.path import join
import numpy as np
import subprocess


def read_split(name):
    path = join(FEATURES_PATH, name)
    with open(path, 'r') as f:
        lines = f.readlines()

    samples = []
    targets = []
    for line in lines:
        split_line = line.split()
        features = [float(split_line[2]), float(split_line[3]), float(split_line[4]), float(split_line[5]), float(split_line[6]), float(split_line[7]), float(split_line[8])]
        targets.append(int(split_line[9]))
        samples.append(features)

    return np.array(samples), np.array(targets)


def read_split_as_dict(name):
    path = join(FEATURES_PATH, name)
    with open(path, 'r') as f:
        lines = f.readlines()

    query_doc = {}
    for line in lines:
        split_line = line.split()
        qID = split_line[0].strip()
        docID = split_line[1].strip()
        features = [float(split_line[2]), float(split_line[3]), float(split_line[4]), float(split_line[5]), float(split_line[6]), float(split_line[7]), float(split_line[8])]
        target = int(split_line[9])
        query_doc.setdefault(qID, {}).setdefault(docID, {}).setdefault('X', features)
        query_doc.setdefault(qID, {}).setdefault(docID, {}).setdefault('Y', target)
    return query_doc


def get_accuracy(X, y, model):
    predictions = model.predict(X)
    true_predictions = 0
    i = 0
    for p in predictions:
        real_label = y[i]
        i += 1
        if p > 0.0:
            pred_label = 1
        else:
            pred_label = 0

        if real_label == pred_label:
            true_predictions +=1

    return true_predictions / len(X)


def classification():
    print "REGRESSION---------------"
    regressor = linear_model.LogisticRegression()
    regressor.fit(X, y)

    print "Test Data Performance: %s" %regressor.score(test_x, test_y)
    print "Training Data Performance: %s" %regressor.score(X, y)

    # print get_accuracy(test_x, test_y, regressor)

    print "SVM----------------------"
    classifier = svm.SVC()
    classifier.fit(X, y)
    print "Test Data Performance: %s" %classifier.score(test_x, test_y)
    print "Training Data Performance: %s" %classifier.score(X, y)


def get_avg_precision(name, split, model):
    query_doc = read_split_as_dict(split)
    results = predict_results(query_doc, model)
    file_name = "{}_{}".format(name, split)
    result_file = join(RESULTS_PATH, file_name)
    string = ''
    for qID, doc_scores in results.iteritems():
        sorted_scores = sorted(doc_scores.items(), key = lambda x: x[1][0], reverse=True)
        i = 0
        for docID, score in sorted_scores:
            i += 1
            string += '{} {} {} {} {} {}\n'.format(qID, "Q0", docID, i, score[0], "Exp")

    with open(result_file, 'w') as r:
        r.write(string)

    process = subprocess.Popen([TREC_EVAL_PATH, '-q', QREL_PATH, result_file], stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(out)


def predict_results(query_doc, model):
    results = {}
    for qID, values in query_doc.iteritems():
        for docID, labels in values.iteritems():
            test_X = np.array(labels['X']).reshape(1, -1)
            results.setdefault(qID, {}).setdefault(docID, model.predict(test_X))
    return results


if __name__ == '__main__':
    X, y = read_split('train')
    # query_doc = read_split_as_dict('test-1')
    # model = linear_model.LinearRegression()
    # model = model.fit(X, y)
    # model = tree.DecisionTreeRegressor()
    # model = model.fit(X, y)
    # model = svm.SVR()
    # model = model.fit(X, y)
    # model = svm.LinearSVR()
    # model = model.fit(X, y)
    model = linear_model.Perceptron(fit_intercept=False, n_iter=30, shuffle=False)
    model = model.fit(X, y)
    get_avg_precision('random', 'test', model)