import json

class GraphReader(object):

    def __init__(self, graph_path):
        self.graph_path = graph_path


    def read(self):
        print "Reading the graph from file: %s" %(self.graph_path)
        with open(self.graph_path, 'r') as f:
            return json.load(f)
