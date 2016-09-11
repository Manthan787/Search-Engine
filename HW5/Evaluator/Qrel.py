from config import *


class Qrel(object):

    values = {}

    def __init__(self, path):
        self.qrel_path = path
        self.get()


    def get(self):
        lines = self.read()
        print len(lines)
        for line in lines:
            split_line = line.split()
            queryID = split_line[QID].strip()
            docID = split_line[DOCID].strip()
            grade = int(split_line[GRADE].strip())
            self.values.setdefault(queryID, {}).setdefault(docID, grade)


    def getAsDict(self):
        return self.values


    def read(self):
        with open(self.qrel_path, 'rU') as f:
            lines = f.readlines()
            return lines


    def isRelevant(self, queryID, docID):
        """
        :param queryID: ID of the query for which a document's relevance is to be fetched
        :param docID: ID of the document
        :return: True if the document is relevant for the given Query, False otherwise.
        """
        try:
            return (self.values[queryID][docID]) > 0
        except:
            return False


    def ret_rel(self, qID, results):
        """
        :param results: a list of retrieved results
        :return: No. of relevant results out of given results
        """
        retrel = 0
        for res in results:
            if self.isRelevant(qID, res):
                retrel += 1
        return retrel


    def total_rel(self, qID):
        vector = self.values[qID]
        total_rel = 0
        for docID, grade in vector.iteritems():
            if grade > 0:
                total_rel += 1
        return total_rel
