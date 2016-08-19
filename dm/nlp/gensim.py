import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

documents = ["Shipment of gold damaged in a fire",
             "Delivery of silver arrived in a silver truck",
             "Shipment of gold arrived in a truck"]

texts = [[word for word in document.lower().split()] for document in documents]

print texts



