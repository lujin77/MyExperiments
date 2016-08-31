#! -*- coding:utf-8 -*-

"""
将搜狗输入法细胞的词，转为补充的专名词典（与jieba已有词典不重复的情况下）
"""

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

BASE_DICT_PATH = "dict/dict.txt.big"
NEW_WORDS_PATH = "dict/new_words.txt"
OUTPUT_DICT_PATH = "dict/sougo.dict.txt"

# 加载jieba库中已有词典的词
dict_exist_words = {}
file_base_dict = open(BASE_DICT_PATH, 'r')
for line in file_base_dict:
    segs = line.strip('\n').split(' ')
    dict_exist_words[segs[0]] = 1
file_base_dict.close()

# 遍历搜狗的词，与jieba已有词排重，属于新词的生成新词词典
new_num = 0;
new_word_list = []
file_new_word = open(NEW_WORDS_PATH, 'r')
for line in file_new_word:
    word = line.strip('\n').strip()
    # jieba已有词典不重复的，作为补充专名生产搜狗的扩展词典
    if not dict_exist_words.has_key(word):
        new_num = new_num + 1
        new_word_list.append("%s 1 nz\n" % (word))
file_new_word.close()

print "new_word_num=" + str(new_num)

fout = open(OUTPUT_DICT_PATH, 'w')
fout.writelines(new_word_list)
fout.close()

print "write new words dict ok !"


