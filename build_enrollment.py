import pandas as pd
import numpy as np
from course_tree import *
from course_tree_node import *

erl = pd.DataFrame(pd.read_csv('./train/enrollment_train.csv',header = 0))
# erl.to_csv('./train/test/a.csv',index = False,index_label= False,header = 1)
log = pd.DataFrame(pd.read_csv('./train/log_train.csv',header = 0))
print log.info()



for idx,row in erl.iterrows():
    cur =  log[log.enrollment_id == row.enrollment_id]
    path = './train/course/' + str(row.enrollment_id) + '.csv'
    cur.to_csv(path,index = False,index_label= False,header = 1)




