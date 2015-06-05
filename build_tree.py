import pandas as pd
import numpy as np
from tree import *
from node import *


df = pd.DataFrame(pd.read_csv('./obj.csv',header = 0))

courses = {}



for id in pd.unique(df.course_id):
	print id
	if not courses.has_key(id):
		course_tree = Tree(id)
		courses[id] = course_tree









for idx,row in df.iterrows():
	course_tree = courses.get(row.course_id)
	insert = Node(row.module_id)
	insert.category = row.category
	#set children for insert
	if pd.notnull(row.children):
		children = []
		children = str(row.children).split(" ")
		children = children[:-1]
		for child in children:
			childNode = Node(child)
			insert.children[child] = None
	course_tree.insert(insert)





for id,tree in courses.items():
	# tree.print_tree()
	tree.get_root().print_weird()

	tree.get_root().find_node("odDUXQbmYQGcdApIJQrK58kiwHmgSuNq").print_parents()



