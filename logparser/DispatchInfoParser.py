#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import multiprocessing
from optparse import OptionParser

KAFKA_TOPIC = "log_test"
KAFKA_GROUP = "logstash"
KAFKA_BROKERS = ['10.0.11.91:9092']

options = {}
args = []


def optParser():
	usage = "usage: python %prog [options] args"
	parser = OptionParser(usage)
	parser.add_option("-v", "--verbose",
					  action="store_true", dest="verbose", default=False,
					  help="make lots of noise [default]")
	parser.add_option("-f", "--filename", type="string", dest="filename", default="dispatch_inf.csv",
					  metavar="FILE", help="write output to FILE")
	parser.add_option("-w", "--worker", type="int", dest="worker", default=multiprocessing.cpu_count(),
					  metavar="INT", help="set num of subprocess to fetch and process data")
	parser.add_option("-d", "--dumper", type="int", dest="dumper", default=1,
					  metavar="INT", help="set num of subprocess to dump file")

	(options, args) = parser.parse_args()

	if options.verbose == True:
		logging.basicConfig(
			level=logging.DEBUG,
			format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
		)
		logging.info("LogLevel=DEBUG")
	else:
		logging.basicConfig(
			level=logging.INFO,
			format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
		)
		logging.info("LogLevel=INFO")

	logging.info("Outfile=%s" % options.filename)
	logging.info("Worker_num=%d" % options.worker)

	return (options, args)



if __name__ == '__main__':

	options, args = optParser()

