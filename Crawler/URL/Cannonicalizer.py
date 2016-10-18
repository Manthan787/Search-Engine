from urlparse import urlsplit
from urlparse import urlunsplit
from URL import URL
import re


class Cannonicalizer (object):

	def __init__(self, url):
		self.url = url


	def cannonicalize(self):
		parsed_url = urlsplit(self.url)	
		url = URL(parsed_url[:])
		self.url = url.make()
		
		if self.url == "":
			return None
		
		self.url = self.url.replace("https://", "http://")		
		self.url = re.sub('#.*', "", self.url)
		
		return self.url	
