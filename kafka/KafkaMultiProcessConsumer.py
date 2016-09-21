# -*- coding:utf-8 -*-


from kafka import MultiProcessConsumer, KafkaClient

import sys
reload(sys)
sys.setdefaultencoding('utf8')

brokers = ["10.0.11.91:9092"]
kafka = KafkaClient(brokers)
consumer = MultiProcessConsumer(kafka, "multiprocess1-group", "test_m", num_procs=4)
print('*** all offsets=%s' % consumer.offsets)
consumed_count = 0
for message in consumer:
	print(message)
	consumed_count += 1

print('*** all offsets=%s ...after consuming all messages, number of messages consumed=%s' % (consumer.offsets, consumed_count))
