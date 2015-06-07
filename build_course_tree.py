import pandas as pd
import pickle
import numpy as np
from course_tree import *
from course_tree_node import *


df = pd.DataFrame(pd.read_csv('./obj2.csv',header = 0))

courses = {}



for id in pd.unique(df.course_id):
	# print id
	if not courses.has_key(id):
		course_tree = CourseTree(id)
		courses[id] = course_tree


for idx,row in df.iterrows():
    course_tree = courses.get(row.course_id)
    insert = CourseTreeNode(row.module_id)
    insert.set_category(row.category)
    insert.set_start(row.start)

    if pd.notnull(row.children):
        children = []
        children = str(row.children).split(" ")
        children = children[:-1]
        for child in children:
            childNode = CourseTreeNode(child)
            insert.children[child] = None
    course_tree.insert(insert)





for id,tree in courses.items():
    tree.print_tree()
    print "--------------------------------------------------------"
    # tree.find("qpnaou37iVOSWvH3P4Kme8n6Ut2eHXNo").print_node()





