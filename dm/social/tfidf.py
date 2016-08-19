#! -*- coding:utf-8 -*-
from gensim import corpora, models, similarities
import jieba
import sys, os, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf-8')

DICT_PATH = "data/deerwester.dict"
CORPUS_PATH = "data/deerwester.mm"

TFIDF_OUT_FILE = "data/tfidf_result.txt"

if (os.path.exists(DICT_PATH)):
    dictionary = corpora.Dictionary.load(DICT_PATH)
    corpus = corpora.MmCorpus(CORPUS_PATH)
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")

tfidf_model = models.TfidfModel(corpus)
corpus_tfidf = tfidf_model[corpus]

test = "海词词典是中国第一个在线词典,海量权威词典官方网站。独有2000万词汇,配释义饼图、精细讲解、优质例句,专业提供60个行业11个语种的在线词典和在线翻译服务。"
result = ""
seg_list = jieba.cut(test)
tfidf = tfidf_model[dictionary.doc2bow(seg_list)]
for turple in tfidf:
        word = dictionary.get(turple[0]).encode("utf-8")
        score = turple[1]
        result = result + "(" + word + ":" + str(score) + ") "
print result
exit(0)
# dictionary.id2token[]

fo = open(TFIDF_OUT_FILE, 'w')
for tfidf in corpus_tfidf:
    #sorted_tfidf = sorted(enumerate(tfidf), key=lambda item: -item[1])
    tfidf.sort(key=lambda x:x[1], reverse=True)
    result = ""
    for turple in tfidf:
        word = dictionary.get(turple[0]).encode("utf-8")
        score = turple[1]
        result = result + "(" + word + ":" + str(score) + ") "
    fo.writelines(result + "\n")
fo.close()

