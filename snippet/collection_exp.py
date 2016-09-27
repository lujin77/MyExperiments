# -*- coding:utf-8 -*-

print "\n[INFO] map/reduce functional example"
from functools import reduce

def str2int(s):

    def fn(x, y):
        return x * 10 + y

    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

    return reduce(fn, map(char2num, s))

print str2int("123456")


print "\n[INFO] namedtuple -> turple的封装"
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print p.x
print p.y


print "\n[INFO] 双端队列"
from collections import deque
q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print q


print "\n[INFO] key不存在时，返回一个默认值"
from collections import defaultdict
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print dd['key1'] # key1存在
print dd['key2'] # key2不存在，返回默认值


print "\n[INFO] OrderedDict的Key会按照插入的顺序排列，不是Key本身排序"
from collections import OrderedDict
d = dict([('a', 1), ('b', 2), ('c', 3)])
print d # dict的Key是无序的
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print od # OrderedDict的Key是有序的


print "\n[INFO] 累加器,实现dict的累计"
from collections import Counter
c = Counter()
for ch in 'programming':
	c[ch] = c[ch] + 1
print c