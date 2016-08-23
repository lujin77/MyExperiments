#! -*- coding:utf-8 -*-
import jieba.analyse

class WordSegger:

    # 定义基本属性
    name = ''
    age = 0
    # 定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0

    # singleton
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(WordSegger, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    # 定义构造方法
    def __init__(self):
        print "[TRACT] begin to load segger dict..."
        jieba.load_userdict("dict/dict.txt.big")
        print "[INFO] load segger dict success"

        print "[TRACT] begin to load analyse dict..."
        jieba.analyse.set_stop_words("dict/stopwords.txt")
        jieba.analyse.set_idf_path("dict/idf.txt.big")
        print "[INFO] load analyse dict success"

    def speak(self):
        print("%s is speaking: I am %d years old" % (self.name, self.age))

o = WordSegger()

