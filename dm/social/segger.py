#! -*- coding:utf-8 -*-
import jieba
import logging
import logging.handlers
import os, sys
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')

jieba.load_userdict("dict/dict.txt.big")
jieba.load_userdict("dict/idf.txt.big")


# seg_list = jieba.cut("我来到北京清华大学", cut_all = True)
# print "Full Mode:", ' '.join(seg_list)
#
# seg_list = jieba.cut("我来到北京清华大学")
# print "Default Mode:", ' '.join(seg_list)

def removeStopWords(stopWords_set, seg_list):
    result_list = []
    remove_num = 0
    for word in seg_list:
        #word = word.encode("utf-8")
        if word in stopWords_set:
            remove_num = remove_num + 1
            continue
        else:
            result_list.append(word)
    # print "removed=" + str(remove_num)
    return result_list


def seg(str):
    global stopWords
    seg_list = jieba.cut(str)
    seg_list = removeStopWords(stopWords, seg_list)
    result = ' '.join(seg_list)
    return result


# 加载停用词
stopWords = []
fi = open('dict/stopwords.txt', 'r')
for line in fi.readlines():
    line = line.strip()
    # 使用unicode对象构造字典
    stopWords.append(unicode(line, "utf-8"))
fi.close()
stopWords = set(stopWords)
print "[INFO] load stop words, size=" + str(len(stopWords))

# 逐条处理语料
fi = open('data/corpus.txt', 'r')
fo = open('data/corpus_segged.txt', 'w')
for line in fi.readlines():
    segs = line.strip().split('\t')
    lineNo = int(segs[0])
    index = int(segs[1])
    title = segs[2]
    content = segs[3]
    cateId = int(segs[4])
    cateName = segs[5]

    #print chardet.detect(cateName)

    # 切词，停用
    title = seg(title)
    content = seg(content)

    #print chardet.detect(title)

    # 组合字符串
    text = "%(lineNo)s\t%(index)s\t%(title)s\t%(content)s\t%(cateId)s\t%(cateName)s" \
           % {'lineNo': lineNo, 'index': index, 'title': title, "content": content, "cateId": cateId,
              "cateName": cateName}
    # text = str(index) + " " + str(date) + " " + title + " -> (" + content + ")"
    print text
    fo.writelines(text + "\n")
fo.close()
fi.close()
