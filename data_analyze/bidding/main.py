# -*- coding:utf-8 -*-

titles = []
with open("title/order.title" ,'r') as fp:
	for line in fp:
		titles.append(line.strip())

print len(titles)
print ','.join(titles)