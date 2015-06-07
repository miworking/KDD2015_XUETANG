import pandas as pd
import numpy as np
from course_tree import *
from course_tree_node import *

enrollment = pd.DataFrame(pd.read_csv('./test/enrollment_test.csv',header = 0))

log = pd.DataFrame(pd.read_csv('./test/log_test.csv',header = 0))


for crs_id in pd.unique(enrollment.course_id):
    cur_enroll = enrollment[enrollment.course_id == crs_id].enrollment_id
    cur_enrolllist = cur_enroll.tolist()
    cur = log[log.enrollment_id.isin(cur_enrolllist)]
    path = './test/course/' + crs_id + '.csv'
    cur.to_csv(path,index = False,index_label= False,header = 1)



