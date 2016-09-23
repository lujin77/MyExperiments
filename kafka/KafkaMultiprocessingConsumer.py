# -*- coding:utf-8 -*-

from kafka import KafkaConsumer
from multiprocessing import Pool
import multiprocessing

import sys

reload(sys)
sys.setdefaultencoding('utf8')


def worker(index):
	consumer = KafkaConsumer('test', group_id='parallel1-group', bootstrap_servers=['10.0.11.91:9092'])
	for message in consumer:
		print ("worker[%s] %s:%d:%d: key=%s value=%s" % (index, message.topic, message.partition,
		                                                 message.offset, message.key,
		                                                 message.value))


if __name__ == "__main__":

	pool = Pool(4)
	for i in xrange(5):
		pool.apply_async(worker, args=(str(i)))

		print("The number of CPU is:" + str(multiprocessing.cpu_count()))

	for p in multiprocessing.active_children():
		print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

	pool.close()
	pool.join()

	print "END!!!!!!!!!!!!!!!!!"
