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
print enrollmentIds

# load classification result
result = pd.DataFrame(pd.read_csv('./train/truth_train.csv',header = 0))

matrix = pd.merge(enrollmentIds,result,on='enrollment_id',how='left')

print matrix

