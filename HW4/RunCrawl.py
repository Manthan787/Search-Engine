from HW4.PageRank.PageRank import PageRank
from HW4.Utils.ESClient import ESClient
from HW4.Utils.Mapper import Mapper
from HW4.Utils.Writer import ResultWriter
from HW4.Utils.Reader import GraphReader
from config import CRAWL_GRAPH_PATH


if __name__ == '__main__':
	client = ESClient()
	reader = GraphReader(CRAWL_GRAPH_PATH)
	graph = reader.read()
	pr = PageRank(graph)
	results = pr.run()
	resultWriter = ResultWriter(results, graph)
	resultWriter.write('crawl_pr')