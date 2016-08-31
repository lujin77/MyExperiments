# -*- coding:utf-8 -*-

"""step 1
从mongodb获取语料的脚本，解析为tsv

输入（mongodb）：
  直接访问mongodb

输出（文件）：
  格式：行号 | 源数据序号 |  标题 | 内容 | 分类id |  分类名
  例子：1	3	当狮子遇上其他星座	今天来讲讲大狮子跟其他星座的火花。[色]	46	穿越

"""

from pymongo import MongoReplicaSetClient
from pymongo import MongoClient
import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

MONGDB_URL = "mongodb://IP:PORT/"
OUTPUT_CORPUS = "data/corpus.txt"


def count(collection, condition):
    """统计行数
        Parameters:
            collection - mongodb的文档集
            condition - mongodb的查询条件
        Returns: 字符串“total=XX， valid=XXX”
        Raises: 无
    """
    total = 0
    valid = 0
    for topic in collection.find(condition):
        total = total + 1
        title = topic.get("topicName", "null")
        content = topic.get("content", "null")
        if len(title) > 5 and len(content) > 20:
            valid = valid + 1
    print "total=" + str(total) + ", valid=" + str(valid)


def getCateTurple(groupId):
    """获取某一个圈子对应的分类信息，包括：分类id、分类层级、分类名
        Parameters:
            groupId - 圈子id
        Returns: 元组（分类id, 分类层级, 分类名）
        Raises: 无
    """
    if groupId == "" or groupId == "null":
        return ("null", "null", "null")

    global socialGroup
    group = socialGroup.find({"_id": groupId})[0]
    cateId = group.get("categoryId", "null")

    if cateId == "null":
        return ("null", "null", "null")

    category = socialCategory.find({"categoryId": cateId})[0]
    cateLv = category.get("categoryLevel", "null")
    cateName = category.get("name", "null")
    return (cateId, cateLv, cateName)


# client = MongoReplicaSetClient("mongodb://10.125.141.131:30000/")
client = MongoClient(MONGDB_URL)

db = client.social
socialTopic = db.socialTopic        # 话题
socialGroup = db.socialGroup        # 圈子
socialCategory = db.socialCategory  # 分类

# count(collection, {"states" : 1, "auditState" : 2.0})

index = 0
lineNo = 0
dict = {}

# 遍历话题，提前原始语料，整理为tsv写到文件
fo = open(OUTPUT_CORPUS, "w")
for topic in socialTopic.find({"states": 1, "auditState": 2.0}):
    title = (topic.get("topicName", "null"))
    title = ''.join(title.split())
    content = topic.get("content", "null")
    content = ''.join(content.split())
    date = str(topic.get("createTime", "null"))
    date = date.split(" ")[0]

    groupId = str(topic.get("groupId", "null")).strip()
    cateTurple = getCateTurple(groupId)
    cateId = cateTurple[0]
    cateLv = cateTurple[1]
    cateName = cateTurple[2]

    index = index + 1

    # 判重
    key = hash(title)
    if dict.get(key) != 1:
        dict.setdefault(key, 1)
        #print title + " size=" + str(len(title))
        if len(title) > 5 and len(content) > 10:
            lineNo = lineNo + 1
            text = "%(lineNo)s\t%(index)s\t%(title)s\t%(content)s\t%(cateId)s\t%(cateName)s" \
                   % {'lineNo': lineNo, 'index': index, 'title': title, "content" : content, "cateId" : cateId, "cateName" : cateName}
            # text = str(index) + " " + str(date) + " " + title + " -> (" + content + ")"
            print text
            fo.writelines(text + "\n")

fo.close()
