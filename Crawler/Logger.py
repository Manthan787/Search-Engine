import logging


def getLogger():

	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	handler = logging.FileHandler('crawl-new.log')
	handler.setLevel(logging.INFO)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	logger.propagate = False
	logger.addHandler(handler)
	return logger
