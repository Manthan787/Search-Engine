from __future__ import division
from HW2.Index.Tokenizer import Tokenizer
from elasticsearch import Elasticsearch
from collections import Counter


query = ['modernist', 'artist']


def score(text):
	avgDocLen = 8000
	tokenizer = Tokenizer(text)
	tokens 	  = tokenizer.tokenize()
	tokenCounts = Counter(tokens)
	docLength = sum(tokenCounts.itervalues())
	nor_length = docLength / avgDocLen

	score = 0
	for w in query:
		tf = tokenCounts.get(w, 0)
		if tf == 0:
			score += 0
		else:
			score += tf / tf + 0.5 + (1.5 * nor_length)

	return score
