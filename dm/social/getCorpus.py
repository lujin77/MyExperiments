# -*- coding:utf-8 -*-
from pymongo import MongoReplicaSetClient
from pymongo import MongoClient
import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

MONGDB_URL = "mongodb://10.125.141.131:30000/"


# 统计行数
def count(collection, condition):
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
socialTopic = db.socialTopic
socialGroup = db.socialGroup
socialCategory = db.socialCategory

# count(collection, {"states" : 1, "auditState" : 2.0})

index = 0
lineNo = 0
dict = {}

fo = open("data/corpus.txt", "w")

# 遍历topic
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
