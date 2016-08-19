# -*- coding:utf-8 -*-
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




