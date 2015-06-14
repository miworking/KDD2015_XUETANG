import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *

course_id = '5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2'
course_path = './train/fullTree/' + str(course_id) + '_moduleIDs.csv'
matrix = pd.DataFrame(pd.read_csv(course_path,header = 0,index_col = 0,dtype={'start':datetime.datetime}))
print matrix.loc['3fcRJtsci2r7Q2HRnCidiemseTs2a6Fq']



