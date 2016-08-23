#! -*- coding:utf-8 -*-
import numpy as np
from sklearn import preprocessing

arr_list = []
list = [1.0, 2.0, 3.0]
arr_list.append(list)
arr = np.array(arr_list)
print arr
# scaler = preprocessing.Normalizer()
# norm_arr = scaler.fit_transform(arr)
norm_arr = preprocessing.normalize(arr_list, norm='max')
print (norm_arr.tolist())