import urllib2
from HTMLParser import HTMLParser
from urlparse import urljoin
from CrawlResult import CrawlResult
from RequestLog import RequestLog
from bs4 import BeautifulSoup
from HW3.URL.Cannonicalizer import Cannonicalizer
from HW3.URL.URL import getHost, getPath
from reppy.cache import RobotsCache
from HW3.Indexer.DocIndexer import DocIndexer
import time
import PageScorer


robots = RobotsCache()
html_parser = HTMLParser()


class Crawler( object ):

	def __init__(self, url, parentWaveNo, reqLog):
		self.url = url	
		self.parentWaveNo = parentWaveNo
		self.reqLog = reqLog


	def crawl(self):		
		
		if not self.__canCrawl():					
			return None


		print "Crawling URL : %s" %self.url		
		
		if time.time() - self.reqLog.mostRecentRequest(self.url) < 1:
			print "Politeness Stop for URL : %s" %self.url
			time.sleep(1)
				
		self.reqLog.add(self.url)
		
		try:
			response = urllib2.urlopen(self.url, timeout=10)		
			headers  = response.info()
		except urllib2.URLError as e:
			print "--------Error Connecting To THE URL: %s" %e			
			return None

		if self.__pageIsHtml(dict(headers)):
			text, title, links, rawHTML = self.__process(response.read(), dict(headers))
			waveNo = self.parentWaveNo + 1						
			content = {'url':self.url, 'text': text, 'title': title, 'headers': str(headers), 'rawHTML': rawHTML}
			parent_score = PageScorer.score(text)
			return CrawlResult(content, links, waveNo, parent_score)
		else:
			# print "The page is not an HTML Page!"
			return None

	
	def __canCrawl(self):		
		# robotPath = "http://{}/robots.txt".format(getHost(self.url))
		# try:
		# 	robot_rules = robots.fetch(robotPath)
		# except Exception as e:
		# 	return True
		try:
			return robots.allowed(self.url, "my-agent")
		except Exception:
			return True

		# return robot_rules.allowed(getPath(self.url), "*")


	def __process(self, rawHTML, headers):	
		''' Process the raw html text '''
		split_headers = headers.get('content-type', "").split(';')		
		if len(split_headers) > 1:
			try:
				encoding = split_headers[1].split('=')[1]
			except Exception:
				encoding = "utf-8"
		else:
			encoding = "utf-8"

		try:
			rawHTML = unicode(rawHTML, encoding)
		except UnicodeDecodeError as ue:
			print "Error while converting RAWHTML to UNICODE : %s" %ue
			pass

		soup = BeautifulSoup(rawHTML, 'lxml')
		try:
			title = soup.title.string
		except AttributeError:
			title = 'No Title Found'
		links = self.__findLinks(soup)
		self.__removeScriptandStyle(soup)
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))		
		text = '\n'.join(chunk for chunk in chunks if chunk)
		return (text, title, links, rawHTML)


	def __removeScriptandStyle(self, soup):
		''' Remove the script tags and style tags within raw HTML '''
		for elem in soup.findAll(['script', 'style']):
			elem.extract()


	def __findLinks(self, soup):
		links = []
		for a in soup.find_all('a', href=True):
			url = urljoin(self.url, a['href'])
			cannonicalizer = Cannonicalizer(url)
			url = cannonicalizer.cannonicalize()			
			links.append(url)

		print "Found %s URLS for %s" %(len(links), self.url)
		return links


	def __pageIsHtml(self, headers):
		content_type = headers.get('content-type', None)
		if content_type is not None:
			if 'text/html' in content_type.split(';'):
				return True

		return False


# reqLog = RequestLog()
# crawler = Crawler("https://en.wikipedia.org", 1, reqLog)
# indexer = DocIndexer({'wiki': crawler.crawl()})
# indexer.index()
