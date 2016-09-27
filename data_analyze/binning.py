# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np

# 分箱:
def binning(col, cut_points, labels=None):

	# Define min and max values:
	minval = col.min()
	maxval = col.max()

	# 利用最大值和最小值创建分箱点的列表
	break_points = [minval] + cut_points + [maxval]

	# 如果没有标签，则使用默认标签0 ... (n-1)
	if not labels:
		labels = range(len(cut_points) + 1)

	# 使用pandas的cut功能分箱
	colBin = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
	return colBin


data =[]
for i in xrange(10):
	tmp = []
	for j in xrange(3):
		tmp.append(np.random.randint(0, 100))
	data.append(tmp)

data = pd.DataFrame(data, columns=["A", "B", "C"])
print data

# 为年龄分箱:
cut_points = [30, 50, 70]
labels = ["low", "medium", "high", "very high"]
data["A_Bin"] = binning(data["A"], cut_points, labels)
print data
print pd.value_counts(data["A_Bin"], sort=False)

data.boxplot(column="A",by="A_Bin")
