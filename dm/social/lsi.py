#! -*- coding:utf-8 -*-
from gensim import corpora, models, similarities
import sys, os, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf-8')

DICT_PATH = "data/deerwester.dict"
CORPUS_PATH = "data/deerwester.mm"

TFIDF_OUT_FILE = "data/lsi_result.txt"

if (os.path.exists(DICT_PATH)):
    dictionary = corpora.Dictionary.load(DICT_PATH)
    corpus = corpora.MmCorpus(CORPUS_PATH)
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")

lsi_model = models.LsiModel(corpus)
corpus_lsi = lsi_model[corpus]

# dictionary.id2token[]

fo = open(TFIDF_OUT_FILE, 'w')
for lsi in corpus_lsi:
    #sorted_tfidf = sorted(enumerate(tfidf), key=lambda item: -item[1])
    lsi.sort(key=lambda x:x[1], reverse=True)
    result = ""
    for turple in lsi:
        word = dictionary.get(turple[0]).encode("utf-8")
        score = turple[1]
        result = result + "(" + word + ":" + str(score) + ") "
    fo.writelines(result + "\n")
fo.close()

