

import threading, logging, time, random
from kafka import KafkaConsumer, KafkaProducer


class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='10.0.11.91:9092')

        while True:
            producer.send('test', "hello world {str}".format(str=str(random.randint(12,20))), "007")
            time.sleep(1)


class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='10.0.11.91:9092',
                                 auto_offset_reset='earliest')
        consumer.subscribe(['test'])

        for message in consumer:
            print ("[TRACE] -> " + str(message))


def main():
    threads = [
        Producer(),
        Consumer()
    ]

    for t in threads:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()