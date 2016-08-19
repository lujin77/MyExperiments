# -*- coding:utf-8 -*-
str = "人生苦短"                     # 一个utf-8格式的字节串
unicodeObj = str.decode("utf-8")     # str被解码为unicode对象，赋给u
str = unicodeObj.encode("utf-8")     # unicodeObj被编码为gbk格式的字节串
print str

str1 = "字符串"
str2 = u"字符串"
print type(str1)
print type(str2)