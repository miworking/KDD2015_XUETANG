import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *



df0 = pd.DataFrame(pd.read_csv('./object.csv',header = 0))
df = df0[df0.course_id == '5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2']

courses = {}



for id in pd.unique(df.course_id):
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





for course_id,tree in courses.items():
	print "------------------------------"
	# tree.print_tree()
	course_path = './train/course/' + str(course_id) + '.csv'
	log = pd.DataFrame(pd.read_csv(course_path,header = 0))
	full_tree = FullTree(tree,course_id)
	output = open('./train/log/5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2.txt','w')
	for idx,row in log.iterrows():
		full_tree.add_access_log(AccessLog(row.object,row.time,row.source,row.event,row.enrollment_id))
	# full_tree.print_tree()
	full_tree.rectify_time()
	full_tree.print_tree_to_file(output)
	output.close
	# pickle.dump(course_enrollment_trees,output,-1)
	# output.close()













