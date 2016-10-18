from HW3.LinkQueue.QueueRetriever import QueueRetriever
from Queue import Queue, Empty
from HW3.LinkQueue.OutlinkBuffer import OutlinkBuffer
from HW3.LinkQueue.Queuer import Queuer
from HW3.Crawler.Crawler import Crawler
from HW3.Crawler.RequestLog import RequestLog
from HW3.Crawler.LinkGraph import LinkGraph
from HW3.Indexer.DocIndexer import DocIndexer
from threading import Thread, current_thread
import timeit
import Logger
from tld import get_tld
import time
import pickle
import sys
from threading import Lock, local
import logging
import socket


# logging.basicConfig()

thread_storage = local()
socket.setdefaulttimeout(10)
lock = Lock()
THREADPOOL_SIZE 			= 20
INDEX_SIZE					= 10000
DOC_INDEX_BUFFER_SIZE 		= 50
OUTLINK_BUFFER_THRESHOLD 	= 7000
crawl_results = {}
graph = LinkGraph()
outlinkbufr = OutlinkBuffer(OUTLINK_BUFFER_THRESHOLD)
visited = 0
queue = Queue()

logger = Logger.getLogger()
logger.info("Starting crawl!")
def indexDocs():
	global crawl_results	
	indexer = DocIndexer(crawl_results)
	indexer.index()
	crawl_results = {}


def indexThreadDocs(results):
	logger.info("Indexing docs in a single thread! - size 100")
	indexer = DocIndexer(results)
	indexer.index()


def main():
	global queue
	reqLog = RequestLog()
	
	for i in range(0, THREADPOOL_SIZE):
			worker = Thread(target=run, args=(reqLog, queue))
			worker.setDaemon(True)			
			worker.start()		
	while visited < INDEX_SIZE: 
		logger.debug("Visited So far %s", visited)		
		retriever = QueueRetriever()
		links = retriever.retrieve()		
		map(queue.put, links)
		queue.put(None)
		queue.join()
		indexDocs()		
		outlinkbufr.enqueueAndFlush()
		graph.store()
	

def run(reqLog, queue):	
	# thread_storage.results = []
	while True:
		try:
			link = queue.get(timeout=15)			
			if link is not None:
				process_link(link, reqLog)
				# if res is not None:
				# 	thread_storage.results.append(res)
				# 	msg = "storage for {} is {}".format(current_thread().name, len(thread_storage.results))
				# 	logger.info(msg)


			# if len(thread_storage.results) >= DOC_INDEX_BUFFER_SIZE:
			# 	# print "Storage for thread %s is %s" %(current_thread().name, len(thread_storage.results))
			# 	results = getattr(thread_storage, 'results', [])
			# 	indexThreadDocs(results)
			# 	thread_storage.results = []
			queue.task_done()
		except Empty as e:
			with queue.mutex:
				queue.all_tasks_done.notify_all()
				queue.unfinished_tasks = 0	
				continue


def process_link(link, reqLog):
	global crawl_results, outlinkbufr, visited	
	parent_waveNo = link['_source']['DISCOVERY_WAVE_NO']
	url = link['_id']		
	crawler = Crawler(url, parent_waveNo, reqLog)
	try:		
		crawl_result = crawler.crawl()	
	except Exception:
		crawl_result = None

	with lock:
		if crawl_result is not None:
			visited += 1
			if len(crawl_results) > DOC_INDEX_BUFFER_SIZE:
				msg = "Length of results: %s" %len(crawl_results)
				logger.info(msg)
				indexDocs()

			url = crawl_result.getUrl()	# get cannonicalized url from the result
			crawl_results[url] = crawl_result		
			links = {url: crawl_result.getLinks()}
			graph.update(links)
			outlinkbufr.add(crawl_result.transformLinks(graph))

			if time.time() - outlinkbufr.creationTime >= 30:				
				outlinkbufr.enqueueAndFlush()
				graph.store()

			# return (url, crawl_result)
		# else:
		# 	return None


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()
	
