import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *



# course_id = 'bWdj2GDclj5ofokWjzoa5jAwMkxCykd6'
course_id = 'bWdj2GDclj5ofokWjzoa5jAwMkxCykd6'
course_tree_path = './train/courseDump/' + course_id + ".txt"
f = open(course_tree_path,'rb')
full_tree = pickle.load(f)
f.close()










