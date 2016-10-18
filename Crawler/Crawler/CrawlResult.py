from tld import get_tld
from urlparse import urlsplit
class CrawlResult(object):

	def __init__(self, content, links, waveNo, parent_score):
		self.content = content
		self.links   = links		
		self.waveNo  = waveNo
		self.parent_score = parent_score

	def getTitle(self):
		return self.content.get('title')


	def getText(self):
		return self.content.get('text')


	def getUrl(self):
		return self.content.get('url')


	def getLinks(self):
		return self.links


	def getHeaders(self):
		return self.content.get('headers')


	def getWaveNo(self):
		return self.waveNo


	def getRawHTML(self):
		return self.content.get('rawHTML')


	def getParentScore(self):
		return self.parent_score


	def transformLinks(self, linkgraph):
		transformed = []
		for link in self.links:
			try:
				tld = get_tld(link)
			except Exception:
				tld = urlsplit(link).netloc

			res = {'_id': link,
				   '_source': {
				   		'VISITED': False,
				   		'VISITED_DOMAIN_NAME': tld,
				   		'DOMAIN_NAME': tld,
				   		'IN_LINK_CNT': linkgraph.inlinkcount(link),
				   		'DISCOVERY_WAVE_NO': self.waveNo,
				   		'PARENT_SCORE': self.parent_score
				   }}
			transformed.append(res)

		return transformed


	def buildDocPayload(self):
		title = self.getTitle()
		text  = self.getText()
		html = self.getRawHTML()
		if isinstance(html, unicode):
			HTML = html
		else:
			HTML = ''		
		headers = self.getHeaders()

		return {
					'TITLE': title,
					'HTML': HTML,
					'TEXT': text,
					'HTTP_HEADERS': headers,											
				}
