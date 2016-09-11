from HW4.config import RESULTS_PATH, PR_RESULT_WINDOW, INLINK_INDEX, OUTLINK_INDEX
from os.path import join
from django.utils.encoding import iri_to_uri
import operator
import math

class ResultWriter(object):
    def __init__(self, results, graph, mapper=None):
        self.results = results
        self.graph  = graph
        self.mapper = mapper


    def write(self, name, inlink_count=True):
        print "Writing Results to file!"
        sqr_ranks = [math.pow(r, 2) for r in self.results.values()]
        rank_sum = sum(sqr_ranks)
        print "Rank Sum is %s" %(rank_sum)
        sorted_results = sorted(self.results.items(), key=operator.itemgetter(1), reverse=True)
        write_path = join(RESULTS_PATH, name)
        agg_rank = 0
        with open(write_path, 'w') as f:
            for page, rank in sorted_results[0: PR_RESULT_WINDOW]:
                agg_rank += rank
                count = self.__getCount(page, inlink_count)
                if self.mapper is not None:
                    page = self.mapper.lookup(page)

                string = "{}\t{}\t{}\n".format(iri_to_uri(page), rank, count)
                f.write(string)

            rank_string = "Sum of Ranks: {}".format(rank_sum)
            f.write(rank_string)


    def __getCount(self, page, inlink_count):
        if inlink_count:
            count = len(self.graph[page][INLINK_INDEX])
        else:
            count = len(self.graph[page][OUTLINK_INDEX])

        return count