from course_tree import *
from full_tree_node import *
from access_log import *
import pickle
import io
import pandas as pd


path = './train/fullTree/bWdj2GDclj5ofokWjzoa5jAwMkxCykd6_moduleIDs.csv'
time = df = pd.DataFrame(pd.read_csv(path,header = 0))
# print time

get_simple = lambda  x : x[: x.find('.')]
time['start'] = time['start'].apply(get_simple)
print time