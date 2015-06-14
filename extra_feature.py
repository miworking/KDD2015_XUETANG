import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *



# load full course tree
course_id = '5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2'
course_tree_path = './train/courseDump/' + course_id + ".txt"
f = open(course_tree_path,'r')
full_tree = pickle.load(f)
f.close()

# load enrollment data
enrollment = pd.DataFrame(pd.read_csv('./train/enrollment_train.csv',header = 0))
enrollmentIds = enrollment[enrollment.course_id == course_id]

del enrollmentIds['username']


# load classification result
result = pd.DataFrame(pd.read_csv('./train/truth_train.csv',header = 0))



# merge enrollment and result to 'matrix', get enrollment_id and their result
matrix = pd.merge(enrollmentIds,result,how='inner',on='enrollment_id')
del matrix['course_id']

#get access log of this course
access_path = './train/course/' + course_id + ".csv"
access = pd.DataFrame(pd.read_csv(access_path,header = 0))
access_grouped= access.groupby('enrollment_id')
# access_grouped['time'].transform(lambda x : x.min())
# get access count for every enrollment id
access_count = access_grouped.count()
del access_count['time']
del access_count['event']
del access_count['source']

access_count = access_count.reset_index()



matrix = pd.merge(matrix,access_count,on="enrollment_id",how='inner')
matrix['access_times'] = matrix.object
del matrix['object']








# write matrix to csv
path = './train/features/' + course_id + '.csv'
matrix.to_csv(path,index = False,index_label= False,header = 1)
