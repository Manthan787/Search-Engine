from config import *
from os.path import join


class ResultsReader(object):

    result = {}

    def read(self, result_file):
        """
        :return: a dict with results of the queries read from the file
        """

        with open(result_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            split_line = line.split()
            queryID = split_line[RESULT_QID].strip()
            docID = split_line[RESULT_DOCID].strip()
            score = float(split_line[RESULT_SCORE].strip())
            self.result.setdefault(queryID, []).append((docID, score))

        for qID, docs in self.result.iteritems():
            sorted_res = sorted(docs, key=lambda tup: tup[1], reverse=True)
            self.result[qID] = [d[0] for d in sorted_res][0:1000]

        return self.result


if __name__ == "__main__":
    reader = ResultsReader()
    print reader.read()
