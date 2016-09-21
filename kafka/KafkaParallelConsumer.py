# -*- coding:utf-8 -*-

from kafka import KafkaConsumer
import multiprocessing


import sys
reload(sys)
sys.setdefaultencoding('utf8')

def worker(index):
	consumer = KafkaConsumer('test_m', group_id='parallel1-group', bootstrap_servers=['10.0.11.91:9092'])
	for message in consumer:
		print ("worker[%s] %s:%d:%d: key=%s value=%s" % (index, message.topic, message.partition,
		                                                 message.offset, message.key,
		                                                 message.value))


if __name__ == "__main__":

	for i in xrange(4):
		p = multiprocessing.Process(target=worker, args=(str(i)))
		p.start()

	print("The number of CPU is:" + str(multiprocessing.cpu_count()))

for p in multiprocessing.active_children():
	print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

print "END!!!!!!!!!!!!!!!!!"
