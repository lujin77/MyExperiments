# -*- coding:utf-8 -*-

import sys, time, random

from kafka import KafkaProducer
from kafka.errors import KafkaError

IS_LOOP = True
# 加载日志
log_list = []
with open("data/dispatch/dispatch_info.log.20160920", "r") as fp:
	for line in fp:
		log_list.append(line)

TOPIC = "log_test"
producer = KafkaProducer(bootstrap_servers=['10.0.11.91:9092'])

size = len(log_list) - 1

if IS_LOOP:
	#while True:
		#msg = log_list[random.randint(0, size)]
	for i in xrange(len(log_list)):
		msg = log_list[i]
		# Asynchronous by default
		future = producer.send(TOPIC, msg)
		print "[TRACE] send -> " + msg

		# # Block for 'synchronous' sends
		try:
			record_metadata = future.get(timeout=10)
		except KafkaError:
			print "[ERROR] get ask failed, msg=" + msg
			pass

		time.sleep(1)
else:
	msg = log_list[random.randint(0, size)]
	#msg = "begin 123.456 end"
	future = producer.send(TOPIC, msg)
	print "[TRACE] single send -> " + msg
	# Block for 'synchronous' sends
	try:
		record_metadata = future.get(timeout=10)
	except KafkaError:
		print "[ERROR] get ask failed, msg=" + msg
