#! -*- coding:utf-8 -*-
from gensim import corpora, models, similarities
import sys, os, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf-8')

DICT_PATH = "data/deerwester.dict"
CORPUS_PATH = "data/deerwester.mm"

TFIDF_OUT_FILE = "data/lda_result.txt"

if (os.path.exists(DICT_PATH)):
    dictionary = corpora.Dictionary.load(DICT_PATH)
    corpus = corpora.MmCorpus(CORPUS_PATH)
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")

lda_model = models.LdaModel(corpus)
corpus_lda = lda_model[corpus]

# dictionary.id2token[]

fo = open(TFIDF_OUT_FILE, 'w')
for lda in corpus_lda:
    #sorted_tfidf = sorted(enumerate(tfidf), key=lambda item: -item[1])
    lda.sort(key=lambda x:x[1], reverse=True)
    result = ""
    for turple in lda:
        word = dictionary.get(turple[0]).encode("utf-8")
        score = turple[1]
        result = result + "(" + word + ":" + str(score) + ") "
    fo.writelines(result + "\n")
fo.close()

