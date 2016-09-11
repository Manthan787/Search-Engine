from HW4.Utils.ESClient import ESClient
from HW4.config import OUTLINK_INDEX, INLINK_INDEX
from tld import get_tld
from urlparse import urlparse
import random
import math
MAX_ITER = 200


class HITS(object):
    d = 200
    esclient = ESClient()
    prev_hub_perplexities = []
    prev_auth_perplexities = []
    auth_converged = False
    hub_converged = False


    def __init__(self, graph):
        self.graph = graph
        self.base_set = []


    def run(self, root_set):
        self.__createBaseSet(root_set)
        print "Base Set Size: %s" %(len(self.base_set))
        # self.__modifyGraph()
        return self.__hubsAndAuthorities()


    def __modifyGraph(self):
        print "Modifying the graph"
        for page in self.base_set:
            links = self.graph[page]
            page_host = urlparse(page).netloc
            new_outlinks = []
            new_inlinks = []

            for outlink in links[OUTLINK_INDEX]:
                if page_host != urlparse(outlink).netloc:
                    new_outlinks.append(outlink)

            for inlink in links[INLINK_INDEX]:
                if page_host != urlparse(inlink).netloc:
                    new_inlinks.append(inlink)

            self.graph[page] = [new_outlinks, new_inlinks]


    def __hubsAndAuthorities(self):
        auth = {}
        hub = {}
        for page in self.base_set:
            auth[page] = 1
            hub[page] = 1

        iteration = 0
        while not self.__convergence(auth, hub):
        # for i in range(0, MAX_ITER):
            iteration += 1
            print "Iterations %s" % iteration
            norm = 0
            # Auth Update
            for page in self.base_set:
                auth[page] = 0

                for inlink in self.__getInlinks(page):
                    auth[page] += hub.get(inlink, 0)

                norm += math.pow(auth[page], 2)

            norm = math.sqrt(norm)

            for page in self.base_set:
                auth[page] /= norm

            norm = 0

            # Hub Update
            for page in self.base_set:
                hub[page] = 0
                for outlink in self.__getOutlinks(page):
                    hub[page] += auth.get(outlink, 0)

                norm += math.pow(hub[page], 2)

            norm = math.sqrt(norm)

            for page in self.base_set:
                hub[page] /= norm
        # new_graph = self.__createGraph()
        return auth, hub


    def __createBaseSet(self, root_set):
        self.base_set += root_set
        # Add Outlinks of each page in the root set into the base set
        for page in root_set:
            self.base_set += self.__getOutlinks(page)

        # Get inlinks
        inlinks = self.__getInlinks(page)
        if len(inlinks) <= self.d:
            self.base_set += inlinks
        else:
            self.base_set += random.sample(inlinks, self.d)

        self.base_set = list(set(self.base_set))


    def __getOutlinks(self, page):
        links = self.graph.get(page, None)
        if not None:
            return links[OUTLINK_INDEX]

        return []


    def __getInlinks(self, page):
        links = self.graph.get(page, None)
        if not None:
            return links[INLINK_INDEX]

        return []


    def __convergence(self, auth, hub):
        if not self.auth_converged:
            print "Calculating Auth Perplexity"
            self.auth_converged = self.__hasConverged(auth, self.prev_auth_perplexities)

        if not self.hub_converged:
            print "Calculating Hub Perplexity"
            self.hub_converged = self.__hasConverged(hub, self.prev_hub_perplexities)

        return self.auth_converged and self.hub_converged


    def __hasConverged(self, ranks, prev_perplexities):
        entropy = 0
        for page, rank in ranks.iteritems():
            try:
                entropy += rank * math.log(rank, 2)
            except ValueError as e:
                pass

        try:
            perplexity = pow(2, -entropy)
        except OverflowError:
            perplexity = float('inf')
        print "Perplexity : %s" % perplexity
        self.__storePerplexity(perplexity, prev_perplexities)
        if len(prev_perplexities) < 4:
            return False

        first = prev_perplexities[0]
        for p in prev_perplexities[1:]:
            diff = abs(first - p)
            print "Difference: %s" % diff
            if not diff <= 1:
                return False

        return True


    def __storePerplexity(self, perplexity, prev_perplexities):
        if len(prev_perplexities) == 4:
            del prev_perplexities[0]

        prev_perplexities.append(perplexity)


    def __createGraph(self):
        internal_graph = {}
        for url in self.base_set:
            outlinks = [item for item in self.graph[url][OUTLINK_INDEX] if item in self.base_set]
            inlinks = [item for item in self.graph[url][INLINK_INDEX] if item in self.base_set]
            internal_graph[url] = [outlinks, inlinks]
        return internal_graph


