#! -*- coding:utf-8 -*-

"""step 4
采用gensim包对向量后的语料计算tfidf模型
计算结果结合词袋模型的词典，转为：明文+权重，输出到文件

输入（文件）：gensim的词袋词典、向量化后的语料文件
  格式：gensim默认格式

输出（文件）：标签词字符串
  格式：字符串
  例子：(狮子:0.621503509601) (讲讲:0.621503509601) (色:0.476934770286)

"""

from gensim import corpora, models, similarities
import jieba
import sys, os, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf-8')

DICT_PATH = "data/deerwester.dict"
CORPUS_PATH = "data/deerwester.mm"

TFIDF_OUT_FILE = "data/tfidf_result.txt"

# 加载转换的词袋词典，及已经词袋化的语料
if (os.path.exists(DICT_PATH)):
    dictionary = corpora.Dictionary.load(DICT_PATH)
    corpus = corpora.MmCorpus(CORPUS_PATH)
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")

# gensim训练tfidf模型，并用模型转换向量化后的语料
tfidf_model = models.TfidfModel(corpus)
corpus_tfidf = tfidf_model[corpus]

# 语料按照tfidf权重逆序，以明文形式输出关键词
fo = open(TFIDF_OUT_FILE, 'w')
for tfidf in corpus_tfidf:
    #sorted_tfidf = sorted(enumerate(tfidf), key=lambda item: -item[1])
    # tfidf结果，按权重逆序排序
    tfidf.sort(key=lambda x:x[1], reverse=True)
    result = ""
    for turple in tfidf:
        # 结合词袋模型的词典，转换明文
        word = dictionary.get(turple[0]).encode("utf-8")
        score = turple[1]
        result = result + "(" + word + ":" + str(score) + ") "
    fo.writelines(result + "\n")
fo.close()

print "all is done, result=" + TFIDF_OUT_FILE

"""
增量数据预测的一个例子
"""
# test = "海词词典是中国第一个在线词典,海量权威词典官方网站。独有2000万词汇,配释义饼图、精细讲解、优质例句,专业提供60个行业11个语种的在线词典和在线翻译服务。"
# result = ""
# seg_list = jieba.cut(test)
# tfidf = tfidf_model[dictionary.doc2bow(seg_list)]
# for turple in tfidf:
#         word = dictionary.get(turple[0]).encode("utf-8")
#         score = turple[1]
#         result = result + "(" + word + ":" + str(score) + ") "
# print result
# exit(0)
# dictionary.id2token[]

