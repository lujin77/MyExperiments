# -*- coding:utf-8 -*-

title_tag = []
title_dict = {}
with open("title/ods_service_order.title", 'r') as fp:
	for i, line in enumerate(fp):
		segs = line.split('\t')
		title_tag.append(segs[0])
		title_dict[segs[0]] = {"name" : segs[1], "type" : segs[2]}

title_size = len(title_tag)
print "title size: " + str(title_size)
print "\ntitle: " + str(title_tag)


example = []
data = []
with open("data/ods_service_order.mini.txt", 'r') as fp:
	for i, line in enumerate(fp):
		segs = line.split('\001')
		if len(segs) == title_size:
			tuple = dict(zip(title_tag,segs))

			# one example
			# asap 取消
			if tuple['status'] == "8" and tuple['is_asap'] == "1":
				example = segs
		else:
			continue
		data.append(tuple)

print "\ndata size: " + str(len(data))

print "\ndict example:"
print data[0]

print "\nseq example:"
for i, line in enumerate(example):
	#print i, title_tag[i], example[i]
	print example[i]

