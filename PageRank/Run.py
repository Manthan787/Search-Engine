from HW4.PageRank.PageRank import PageRank
from HW4.Utils.Parser import GraphFromFile
from HW4.Utils.Writer import ResultWriter


if __name__ == '__main__':
	graph = GraphFromFile()
	pr = PageRank(graph)
	results = pr.run()
	resultWriter = ResultWriter(results, graph)
	resultWriter.write('wt2g_PR')
	

