from os.path import join
from ..config import *
import random

TRAIN_SET_SIZE = 20


def split_data(scores):
    qIDs = scores.keys()
    train_keys = random.sample(qIDs, TRAIN_SET_SIZE)
    test_keys = [key for key in qIDs if key not in train_keys]
    print train_keys, test_keys
    train = {}
    test = {}
    for key in train_keys:
        train[key] = scores[key]

    for key in test_keys:
        test[key] = scores[key]

    return train, test


def split_from_test(scores, test):
    '''Creates splits by taking a list of test set QueryIDs.
       IDs not in the given test are train IDs '''
    train = [ID for ID in scores if ID not in test]
    test_set = {}
    train_set = {}
    for ID in test:
        test_set[ID] = scores[ID]

    for ID in train:
        train_set[ID] = scores[ID]

    return train_set, test_set


def scores_from_file(name):
    scores_file = join(FEATURES_PATH, name)
    with open(scores_file, 'r') as f:
        lines = f.readlines()
    scores = {}

    for line in lines:
        split_line = line.split()
        qID = split_line[0].strip()
        docID = split_line[1].strip()
        features = [float(split_line[2]), float(split_line[3]), float(split_line[4]), float(split_line[5]), float(split_line[6]), float(split_line[7]), float(split_line[8])]
        target = int(split_line[9])
        scores.setdefault(qID, {}).setdefault(docID, {}).setdefault('X', features)
        scores.setdefault(qID, {}).setdefault(docID, {}).setdefault('Y', target)
    return scores


def write_to_file(scores, name):
    print "Writing features to file"
    string = ''
    for qID, doc_scores in scores.iteritems():
        for dID, labels in doc_scores.iteritems():
            data = []
            data.append(qID)
            data.append(dID)
            for val in labels['X']:
                data.append(val)
            data.append(labels['Y'])
            string += "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n".format(*data)

    path = join(FEATURES_PATH, name)
    with open(path, 'w') as f:
        f.write(string)


def formatter_from_features(X, Y):
    data =  {}
    i = 0
    for val in X:
        data[i] = val
        i += 1

    data[i] = Y

    return data

if __name__ == "__main__":
    scores = scores_from_file('features')
    train, test = split_data(scores)
    train, test = split_from_test(scores, ['93', '100', '97', '58', '56'])
    write_to_file(train, 'train')
    write_to_file(test, 'test')
