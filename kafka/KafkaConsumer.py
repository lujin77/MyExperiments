# -*- coding:utf-8 -*-


from kafka import KafkaConsumer

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# To consume latest messages and auto-commit offsets
# consumer = KafkaConsumer('test',
#                          group_id='test1-group',
#                          bootstrap_servers=['10.0.11.91:9092'])

consumer = KafkaConsumer('dispatch_detail_info', bootstrap_servers=['10.0.11.91:9092'])

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))


# # consume earliest available messages, dont commit offsets
# KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)
#
# # consume json messages
# KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))
#
# # consume msgpack
# KafkaConsumer(value_deserializer=msgpack.unpackb)
#
# # StopIteration if no message after 1sec
# KafkaConsumer(consumer_timeout_ms=1000)
#
# # Subscribe to a regex topic pattern
# consumer = KafkaConsumer()
# consumer.subscribe(pattern='^awesome.*')
#
# # Use multiple consumers in parallel w/ 0.9 kafka brokers
# # typically you would run each on a different server / process / CPU
# consumer1 = KafkaConsumer('test',
#                           group_id='test-group',
#                           bootstrap_servers='my.server.com')
# consumer2 = KafkaConsumer('test',
#                           group_id='test-group',
#                           bootstrap_servers='my.server.com')