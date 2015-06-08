import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *

f = open('./train/courseDump/5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2.txt','r')
full_tree = pickle.load(f)
full_tree.test_print()
full_tree.get_root().test_print()


f.close()
