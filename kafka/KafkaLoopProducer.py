import time
from kafka import KafkaProducer
from kafka.errors import KafkaError

ISOTIMEFORMAT = '%Y-%m-%d %X'

producer = KafkaProducer(bootstrap_servers=['10.0.11.91:9092'])

while True:

	msg = 'hello world {time}'.format(time=time.strftime(ISOTIMEFORMAT, time.localtime()))
	# Asynchronous by default
	future = producer.send('test', msg)
	print "send -> " + msg

	# # Block for 'synchronous' sends
	try:
		record_metadata = future.get(timeout=10)
	except KafkaError:
		# Decide what to do if produce request failed...
		log.exception()
		pass

	time.sleep(5)
