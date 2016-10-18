from HW3.config import elastic_host
from Queuer import Queuer
from QueueRetriever import QueueRetriever
from config import INDEX, TYPE
from Throttler import Throttler
import threading
from threading import Lock, current_thread
import time
from elasticsearch import Elasticsearch

es = Elasticsearch([elastic_host])

class OutlinkBuffer(object):

	def __init__(self, threshold):
		self.linkbuffer = []
		self._lock 	= Lock()
		self.threshold = threshold
		self.creationTime = time.time()

	def add(self, links):	
		self.linkbuffer += links


	def enqueueAndFlush(self):
		# print "Thread trying to get the lock : %s" %(threading.currentThread().getName())
		with self._lock:			
			buffer_length = len(self.linkbuffer)
			if buffer_length > 0:				
				queuer = Queuer(self.linkbuffer)
				queuer.enqueue()
				self.creationTime =  time.time()
				self.linkbuffer = []
				throttler = Throttler()
				throttler.throttle()		


	def updateTime(self):
		self.creationTime = time.time()