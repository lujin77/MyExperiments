import sys
import urllib
import urllib2
import json
import httplib
import random
import threading
import time

ISO_TIME_FORMAT = '%Y-%m-%d %X'
URL = 'http://api.homepage.recom.pro.gomeplus.com/RecommEngine-api/choicest'


def requestRestAPI(url, argsDict, isPost=False):
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    try:
        if isPost:
            params = json.dumps(argsDict)
            req = urllib2.Request(url, params, headers)
        else:
            url += "?" + urllib.urlencode(argsDict)
            # print url
            req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data_str = response.read()
        decoded_data = json.loads(data_str)
        return decoded_data
    except urllib2.URLError, e:
        print e


def test(threadIndex):
    lines = 0
    size = len(lst_user_id) - 1
    mapArgs = {"userId": "0"}
    while True:
        index = random.randint(0, size)
        if index == 0:
            urllib2.Request(URL)
        else:
            mapArgs["userId"] = lst_user_id[index]
            requestRestAPI(URL, mapArgs)
        time.sleep(0.1)
        # record
        lines = lines + 1
        if lines % 10 == 0:
            print "%s thread %s request %d times" % (
            time.strftime(ISO_TIME_FORMAT, time.localtime()), threadIndex, lines)


lst_user_id = []

if __name__ == '__main__':

    print "load user id from file"
    f = open('user_id.txt', 'r')
    for id in f:
        lst_user_id.append(id.strip('\n'))

    print "user-id size:%d id_1=%s id_2=%s id_3=%s" % (len(lst_user_id), lst_user_id[0], lst_user_id[1], lst_user_id[2])

    print "start to request using threading ..."

    threads = []

    for i in xrange(10):
        threads.append(threading.Thread(target=test, args=(i,)))
        time.sleep(random.random())
        threads[i].setDaemon(True)
        threads[i].start()

    print "all threads are started"

    for j in xrange(10):
        threads[j].join()
        print "%s thread %d after join" % (time.strftime(ISO_TIME_FORMAT), j)

    print "exit bench test"
