#! -*- coding:utf-8 -*-

"""step 3
采用gensim包对语料进行向量化，转换为词袋模型
词典的词典、向量化后的语料写入文件，供后续步骤使用

输入（文件）：分词后的语料文件
  格式：行号 | 源数据序号 |  分词后的标题（“ ”连接） | 分词后的内容（“ ”连接） | 分类id |  分类名
  例子：1	3	'狮子 遇上 星座'    '讲讲 狮子 星座 火花 色'	46	穿越

输出（文件）：gensim的词袋词典、向量化后的语料文件
  格式：gensim默认格式

"""

from gensim import corpora
from collections import defaultdict
import os, sys
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

reload(sys)
sys.setdefaultencoding('utf-8')

# 提取文档集合，输入格式为tsv：行号 | 源数据序号 |  分词后的标题（“ ”连接） | 分词后的内容（“ ”连接） | 分类id |  分类名
# 例子： 1    2   '测试 标题'    '测试 内容'    1   体育
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


