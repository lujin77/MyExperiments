#! -*- coding:utf-8 -*-
from gensim import corpora
from collections import defaultdict
import os, sys
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf-8')

# 提取文档集合
fi = open('data/corpus_segged.txt', 'r')
texts = []
titles = []
cateNames = []
for line in fi:
    segs = line.strip().split("\t")
    lineNo = int(segs[0])
    index = int(segs[1])
    title = segs[2]
    content = segs[3]
    cateId = int(segs[4])
    cateName = segs[5]

    text = content.split(" ")
    texts.append(text)

    titles.append(title)
    cateNames.append(cateName)

fi.close()

# 去掉只出现一次的单词
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1] for text in texts]

# 将文档存入字典，字典有很多功能，比如
# diction.token2id 存放的是单词-id key-value对
# diction.dfs 存放的是单词的出现频率
dictionary = corpora.Dictionary(texts)
dictionary.save('data/deerwester.dict')  # store the dictionary, for future reference
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('data/deerwester.mm', corpus)  # store to disk, for later use
#corpus = corpora.MmCorpus('data/deerwester.mm')

for doc in corpus:
    print(doc)


