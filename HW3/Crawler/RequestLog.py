import time
from tld import get_tld
from urlparse import urlsplit
from threading import Lock

class RequestLog(object):

	def __init__(self):
		self.log = {}
		self._lock = Lock()

	def mostRecentRequest(self, url):
		with self._lock:
			tld = self.__tldify(url)
			return self.log.get(tld, 100)


	def add(self, url):
		tld = self.__tldify(url)
		currentTime = time.time()
		self.log[tld] = currentTime


	def __tldify(self, url):
		try:
			tld = get_tld(url)
		except Exception:
			tld = urlsplit(url).netloc

		return tld