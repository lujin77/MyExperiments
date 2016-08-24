#! -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

BASE_DICT_PATH = "dict/dict.txt.big"
NEW_WORDS_PATH = "dict/new_words.txt"
OUTPUT_DICT_PATH = "dict/sougo.dict.txt"

dict_exist_words = {}
file_base_dict = open(BASE_DICT_PATH, 'r')
for line in file_base_dict:
    segs = line.strip('\n').split(' ')
    dict_exist_words[segs[0]] = 1
file_base_dict.close()

new_num = 0;
new_word_list = []
file_new_word = open(NEW_WORDS_PATH, 'r')
for line in file_new_word:
    word = line.strip('\n').strip()
    if not dict_exist_words.has_key(word):
        new_num = new_num + 1
        new_word_list.append("%s 1 nz\n" % (word))
file_new_word.close()

print "new_word_num=" + str(new_num)

fout = open(OUTPUT_DICT_PATH, 'w')
fout.writelines(new_word_list)
fout.close()

print "write new words dict ok !"


