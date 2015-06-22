import pandas as pd
import pickle
import numpy as np
import os
from course_tree import *
from full_tree import *
from full_tree_node import *



df = pd.DataFrame(pd.read_csv('./object.csv',header = 0))

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
	tree = courses[course_id]
	course_path = './train/course/' + str(course_id) + '.csv'
	log = pd.DataFrame(pd.read_csv(course_path,header = 0))
	full_tree = FullTree(tree,course_id)
	print str(course_id)
	for idx,row in log.iterrows():
		full_tree.add_access_log(AccessLog(row.object,row.time,row.source,row.event,row.enrollment_id))
	full_tree.update()












