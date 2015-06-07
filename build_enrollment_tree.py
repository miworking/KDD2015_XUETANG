import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from enrollment_tree_node import *
from enrollment_tree import *



df = pd.DataFrame(pd.read_csv('./obj4.csv',header = 0))

courses = {}



for id in pd.unique(df.course_id):
	# print id
	if not courses.has_key(id):
		course_tree = CourseTree(id)
		courses[id] = course_tree

df_true = pd.DataFrame(pd.read_csv('./train/truth_train.csv',header = 0))


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
	tree.print_tree()
	course_enrollment_trees = {}
	course_path = './train/course/' + str(course_id) + '.csv'
	log = pd.DataFrame(pd.read_csv(course_path,header = 0))

	log_path = './train/log/' + str(course_id) + '.pk'
	# output = open(log_path,'wb')
	for enroll_id in pd.unique(log.enrollment_id):
		print ">>>>>>>>>> " + str(enroll_id) + "  <<<<<<<<<<<" + str(df_true[df_true.enrollment_id == enroll_id].result)

		cur = log[log.enrollment_id == enroll_id]
		course_enrollment_tree = Enrollment_Tree(tree,enroll_id)
		for idx,row in cur.iterrows():
			course_enrollment_tree.add_access_log(AccessLog(row.object_id,row.time,row.source,row.event,row.enrollment_id))
		course_enrollment_trees[enroll_id] =  course_enrollment_tree

		# course_enrollment_tree.print_tree()
	# pickle.dump(course_enrollment_trees,output,-1)
	# output.close()













