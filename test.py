import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *
import datetime






course_id = '5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2'
course_path = './train/course/' + course_id + ".csv"
access = pd.DataFrame(pd.read_csv(course_path,header = 0))
dfg= access.groupby('enrollment_id')

dfg['time'].transform(lambda x : x.min())


count = dfg.count()






# get all unique enrollment_id in this course
id = pd.DataFrame({'enrollment_id':pd.unique(access.enrollment_id)})
# print id

# get result column
result_path = './train/truth_train.csv'
allresult = pd.DataFrame(pd.read_csv(result_path,header = 0))

#get result for this course
this_result = pd.merge(id,allresult,on='enrollment_id',how='left')

# get all visit times
feature = this_result.join(count.time,how='inner',on='enrollment_id')
feature['visit_times'] = feature['time']
del feature['time']
# print feature


module_path = './train/fullTree/' + course_id + "_moduleIds.csv"
modules = pd.DataFrame(pd.read_csv(module_path,header = 0))
videos = modules[modules.category == 'video']

videolist = videos.module_id.tolist()

# mask = access['object'].isin videolist




time = datetime.datetime(2014,10,2,10,0,34)
print time






















