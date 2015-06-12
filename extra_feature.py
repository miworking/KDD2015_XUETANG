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



# merge enrollment and result to 'matrix'
matrix = pd.merge(enrollmentIds,result,how='inner',on='enrollment_id')
del matrix['course_id']





#extra video visit times
video_visit_times = []
for idx, row in matrix.iterrows():
    video_visit_times.append(full_tree.get_video_visite_times(row.enrollment_id))
matrix['video_visit_times'] = video_visit_times


#extra problems visit times
problems_visit_times = []
for idx, row in matrix.iterrows():
    problems_visit_times.append(full_tree.get_problems_visite_times(row.enrollment_id))
matrix['problems_visit_times'] = problems_visit_times

path = './train/features/' + course_id + '.csv'
matrix.to_csv(path,index = False,index_label= False,header = 1)




# write matrix to csv
path = './train/features/' + course_id + '.csv'
matrix.to_csv(path,index = False,index_label= False,header = 1)
