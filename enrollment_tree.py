from course_tree import *
from enrollment_tree_node import *
from access_log import *

class Enrollment_Tree(object):

    def __init__(self):
        self.enrollment_id = None
        self.root = Enrollment_Tree_Node()

    def __init__(self,course_tree,enrollment_id):
        self.enrollment_id = enrollment_id
        self.root = course_tree.root.copy_to_ETNode()

    def add_access_log(self,access_record):
        id = access_record.get_id()
        node = self.root.find_node(id)
        if node is None:
            node = Enrollment_Tree_Node(id)
            node.set_level(1)
            node.category = 'unknown'
            self.root.children[access_record.get_id()] = node
        node.add_access_log(access_record)

    def print_tree(self):
        print "=======================================" + str(self.enrollment_id)
        for id,child in self.root.children.items():
            if child is None:
                print '(' + id + ')'
            else:
                child.print_node_and_children()


