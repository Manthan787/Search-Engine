from urlparse import urlunsplit, urlsplit


# CONSTANTS
SCHEME 		= 0
HOST   		= 1
PATH   		= 2
QUERY  		= 3
FRAGMENT 	= 4

class URL (object):


	def __init__(self, components):
		self.components = components


	def make(self):
		scheme 		= self.components[SCHEME].lower()
		host   		= self.components[HOST].lower()
		path   		= self.components[PATH]
		query  		= self.components[QUERY]
		fragment 	= self.components[FRAGMENT]
		return urlunsplit([scheme, host, path, query, fragment])


# Module methods
def getHost(url):
	return urlsplit(url).netloc


def getPath(url):
	return urlsplit(url).path
