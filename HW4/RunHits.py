from HW4.HITS.HITS import HITS
from HW4.Utils.ESClient import ESClient
from HW4.Utils.Mapper import Mapper
from HW4.Utils.Writer import ResultWriter
from HW4.Utils.Reader import GraphReader
from config import *
import json


def readGraph():
    print "Loading Graph!"
    with open(CRAWL_GRAPH_PATH, 'r') as f:
        return json.load(f)


client = ESClient()
# graph  = client.getGraph()
reader = GraphReader(CRAWL_GRAPH_PATH)
graph = reader.read()

print "Getting the root set!"
root_set = client.getRootSet()
hits = HITS(graph)
auth, hub = hits.run(root_set)

resultWriter = ResultWriter(auth, graph)
resultWriter.write('auth_score_x')

resultWriter = ResultWriter(hub, graph)
resultWriter.write('hub_score_x', inlink_count=False)
