#! -*- coding:utf-8 -*-
import sys
import jieba
import jieba.analyse

reload(sys)
sys.setdefaultencoding('utf-8')

partOfSpeech = ('n', 'nr', 'ns', 'nt', 'nz', 'nrt', 'j', 'b', 'v', 'vn', 'ng')

jieba.load_userdict("dict/dict.txt.big")
jieba.load_userdict("dict/ext_dict.txt")
#jieba.add_word('小蛮腰')
test_str = "7天快速塑造迷人小蛮腰"
print ' ' .join(jieba.cut(test_str))

print ' ' .join(jieba.analyse.extract_tags(test_str, topK=10))
print ' ' .join(jieba.analyse.extract_tags(test_str, topK=10, allowPOS=partOfSpeech))

# partOfSpeech=('n','an', 'ns', 'vn', 'nz', 'nr', 'nrt', 'ns', 'nt','j','b')
# tags = jieba.analyse.extract_tags(test_str, topK=3, withWeight=True, allowPOS=partOfSpeech, withFlag=True)
# for tag in tags:
#     obj = tag[0]
#     print obj.word + " " + obj.flag


