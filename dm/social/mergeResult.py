# -*- coding:utf-8 -*-

"""step 5
合并原始语料内容，和生成的标签词，便于比对生成效果

输入1（文件）：原始语料文件
  格式：行号 | 源数据序号 |  标题 | 内容 | 分类id |  分类名
  例子：1	3	当狮子遇上其他星座	今天来讲讲大狮子跟其他星座的火花。[色]	46	穿越

输入2（文件）：gensim生产的关键词文件
  格式：字符串
  例子：'(狮子:0.621503509601) (讲讲:0.621503509601) (色:0.476934770286)'

输出（文件）：2个文件按列合并的内容
  格式：行号 | 标题 | 内容 | 关键词及权重
  例子：1	当狮子遇上其他星座	今天来讲讲大狮子跟其他星座的火花。[色]	穿越	(狮子:0.621503509601) (讲讲:0.621503509601) (色:0.476934770286)


"""

import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

SOURCE_FILE = "data/corpus.txt"
TAG_FILE = "data/tfidf_result.txt"
OUT_FILE = "data/merge_result.txt"

tag_list = []
fi_tag = open(TAG_FILE, "r")
for line in fi_tag:
    tag_list.append(line)
fi_tag.close()

fi_src = open(SOURCE_FILE, "r")
fout = open(OUT_FILE, "w")
index = 0;
for line in fi_src:
    segs = line.strip().split('\t')
    title = segs[2]
    content = segs[3]
    cateName = segs[5]

    tag = tag_list[index]
    index = index + 1

    # 组合字符串
    text = "%(index)s\t%(title)s\t%(content)s\t%(cateName)s\t%(tag)s" \
           % {'index': index, 'title': title, 'content': content, "cateName": cateName, "tag": tag.strip()}
    # text = str(index) + " " + str(date) + " " + title + " -> (" + content + ")"
    print text
    fout.writelines(text + "\n")
fi_src.close()
fout.close()




