#! -*- coding:utf-8 -*-

"""step 2
原始语料分词，调用jieba分词库对语料的title和content进行切词

输入（文件）：语料文件
  格式：行号 | 源数据序号 |  标题 | 内容 | 分类id |  分类名
  例子：1	3	当狮子遇上其他星座	今天来讲讲大狮子跟其他星座的火花。[色]	46	穿越

输出（文件）：标签词字符串
  格式：行号 | 源数据序号 |  分词后的标题（“ ”连接） | 分词后的内容（“ ”连接） | 分类id |  分类名
  例子：1	3	'狮子 遇上 星座'    '讲讲 狮子 星座 火花 色'	46	穿越

"""

import jieba
import logging
import logging.handlers
import os, sys
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')

# 加载jieba的词典
jieba.load_userdict("dict/dict.txt.big")
jieba.load_userdict("dict/idf.txt.big")


def removeStopWords(stopWords_set, seg_list):
    """分词结果移出停用词
        Parameters:
            stopWords_set - 停用词集合，dict类型
            seg_list - 分词后的词list
        Returns: list，里面存词
        Raises: 无
    """
    result_list = []
    remove_num = 0
    for word in seg_list:
        # word = word.encode("utf-8")
        if word in stopWords_set:
            remove_num = remove_num + 1
            continue
        else:
            result_list.append(word)
    # print "removed=" + str(remove_num)
    return result_list


def seg(str):
    """采用jieba分词库切词，然后用自定义的停用词表过滤，分词后的结果用“ ”连接成字符串后返回
        Parameters:
            str - 待分词的原始字符串
        Returns: 字符串，最终的分词结果用“ ”连接
        Raises: 无
    """
    global stopWords
    seg_list = jieba.cut(str)
    seg_list = removeStopWords(stopWords, seg_list)
    result = ' '.join(seg_list)
    return result


# 加载停用词，加载的文件格式如下：
# word1
# word2
# ……
stopWords = []
fi = open('dict/stopwords.txt', 'r')
for line in fi.readlines():
    line = line.strip()
    # 使用unicode对象构造字典
    stopWords.append(unicode(line, "utf-8"))
fi.close()
stopWords = set(stopWords)
print "[INFO] load stop words, size=" + str(len(stopWords))

# 逐条处理语料，对标题和内容分词，写入文件
# 输入语料格式为tsv： 行号 | 源数据序号 |  标题 | 内容 | 分类id |  分类名
# 例子： 1    2   测试标题    测试内容    1   体育
fi = open('data/corpus.txt', 'r')                # 待分词的语料
fo = open('data/corpus_segged.txt', 'w')        # 分词后的语料
for line in fi.readlines():
    segs = line.strip().split('\t')
    lineNo = int(segs[0])
    index = int(segs[1])
    title = segs[2]
    content = segs[3]
    cateId = int(segs[4])
    cateName = segs[5]

    # print chardet.detect(cateName)

    # 切词，停用词过滤，用“ ”连接为字符串
    title = seg(title)
    content = seg(content)

    # print chardet.detect(title)

    # 组合字符串
    text = "%(lineNo)s\t%(index)s\t%(title)s\t%(content)s\t%(cateId)s\t%(cateName)s" \
           % {'lineNo': lineNo, 'index': index, 'title': title, "content": content, "cateId": cateId,
              "cateName": cateName}
    # text = str(index) + " " + str(date) + " " + title + " -> (" + content + ")"
    print text
    fo.writelines(text + "\n")
fo.close()
fi.close()
