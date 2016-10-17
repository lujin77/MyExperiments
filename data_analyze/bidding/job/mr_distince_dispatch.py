# -*- coding:utf-8 -*-

from mrjob.job import MRJob
import time


class MROrderTrade(MRJob):

	def mapper(self, _, line):
		# split log
		try:
			yield line, None
		except ValueError, e:
			print e.message, e.args
			self.increment_counter("MROrderTrade", "log_parse_error", amount=1)

	def reducer(self, key, values):
		one = ""
		for value in values:
			one = value
			break
		yield None, value


if __name__ == '__main__':
	MROrderTrade.run()
