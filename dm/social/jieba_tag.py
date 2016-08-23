#! -*- coding:utf-8 -*-
import sys
import chardet
import jieba.analyse
import numpy as np
from sklearn import preprocessing

reload(sys)
sys.setdefaultencoding('utf-8')


def gen_label(sentence, method, type):
    global tags_dict

    # 根据输入决定的参数
    weight_rate = 1.0
    topN = 5;
    if type == "title":
        rate = 1.0
        # utf-8 string is 3 bytes
        # print sentence + " size=" + str(len(sentence))
        str_len = len(sentence) / 3
        if str_len <= 4:
            topN = 1
        elif str_len <= 8:
            topN = 2
        else:
            topN = 3
    elif type == "content":
        rate = 0.8
        str_len = len(sentence) / 3
        if str_len <= 10:
            topN = 3
        elif str_len <= 20:
            topN = 5
        else:
            topN = 8
    else:
        print "[ERROR] input type is invalid, method=" + type
        exit(-1)

    partOfSpeech = ('n', 'nr', 'ns', 'nt', 'nz', 'nrt', 'j', 'b', 'vn', 'ng')

    # invoke jieba to get result
    tags = []
    if method == "tfidf":
        tags = jieba.analyse.extract_tags(sentence, topK=topN, withWeight=True, allowPOS=partOfSpeech, withFlag=True)
        arr_list = []
        weights = [turple[1] for turple in tags]
        weights.append(0.0)     # 占位符，防止最小值被归一化为0
        arr_list.append(weights)
        arr = np.array(arr_list)
        norm_arr = preprocessing.normalize(arr_list, norm='max')
        tmp_list = []
        for i, turple in enumerate(tags):
            tmp_list.append((turple[0], norm_arr[0, i]))
        tags = tmp_list
    elif method == "textrank":
        tags = jieba.analyse.textrank(sentence, topK=topN, withWeight=True, allowPOS=partOfSpeech, withFlag=True)
    else:
        print "[ERROR] input method is invalid, method=" + method
        exit(-1)

    # orignal result
    tag_str_list = ["%s[%s]:%.2f" % (turple[0].word, turple[0].flag, turple[1]) for turple in tags]
    tag_str = ' '.join(tag_str_list)

    # merge result
    for turple in tags:
        key = "%s[%s]" % (turple[0].word, turple[0].flag)
        if tags_dict.get(key, "null") != "null":
            old_score = tags_dict.get(key)
            add_score = turple[1] * weight_rate
            score = old_score + add_score
            tags_dict[key] = score
        else:
            tags_dict[key] = (turple[1] * weight_rate)

    return tag_str


print "[TRACT] begin to load segger dict..."
jieba.load_userdict("dict/dict.txt.big")
jieba.load_userdict("dict/ext_dict.txt")
print "[INFO] load segger dict success"

print "[TRACT] begin to load analyse dict..."
jieba.analyse.set_stop_words("dict/stopwords.txt")
jieba.analyse.set_stop_words("dict/ext_stopwords.txt")
jieba.analyse.set_idf_path("dict/idf.txt.big")
print "[INFO] load analyse dict success"

# 逐条处理语料
fi = open('data/corpus.txt', 'r')
fo = open('data/corpus_tag.txt', 'w')
for line in fi.readlines():
    segs = line.strip().split('\t')
    lineNo = int(segs[0])
    index = int(segs[1])
    title = segs[2]
    content = segs[3]
    cateId = int(segs[4])
    cateName = segs[5]

    tags_dict = {}

    # tfidf tags for title
    tags_str1 = gen_label(title, "tfidf", "title")

    # textrank tags for title
    tags_str2 = gen_label(title, "textrank", "title")

    # tfidf tags for content
    tags_str3 = gen_label(content, "tfidf", "content")

    # textrank tags for content
    tags_str4 = gen_label(content, "textrank", "content")

    # merge result sort and extract
    tmp = []
    for k, v in tags_dict.iteritems():
        tmp.append((k.encode("utf-8"), v))
    tmp.sort(key=lambda x: x[1], reverse=True)
    tmp = ["%s:%.2f" % (tag[0], tag[1]) for tag in tmp]
    tags_str0 = ' '.join(tmp)

    # 组合字符串
    text = "%(lineNo)s\t[%(cateName)s]\t【%(title)s】\tmerge:【%(tags_str0)s】\tt_f:【%(tags_str1)s】\tt_r:【%(tags_str2)s】" \
           "\tc_t:【%(tags_str3)s】\tc_r:【%(tags_str4)s】\t%(content)s" \
           % {'lineNo': lineNo, 'cateName': cateName, "tags_str0": tags_str0, "tags_str1": tags_str1,
              "tags_str2": tags_str2, "tags_str3": tags_str3, "tags_str4": tags_str4, 'title': title,
              "content": content}
    # text = str(index) + " " + str(date) + " " + title + " -> (" + content + ")"
    print text
    fo.writelines(text + "\n")
fo.close()
fi.close()
