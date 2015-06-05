from node import *

class Tree(object):
    def __init__(self,course_id,root):
        self.course_id = course_id
        self.root = root

    def __init__(self,course_id):
        self.course_id = course_id
        self.root = Node(0)
        self.root.level = 0
        self.root.parent = None

    def get_courseid(self):
        return self.course_id

    def get_root(self):
        return self.root

    def insert(self,node):
        insert_new = True
        for child in self.root.get_children().values():
            if child.insert(node):
                insert_new = False
                break

        if insert_new:
            self.root.get_children()[node.id] = node
            node.level = 1
            node.parent = self.root
            # print node.id




    def print_tree(self):
        print "----TREE--" + self.course_id + "------"
        for id,child in self.root.get_children().items():
            if child is None:
                print "(" + id + ")"
            else:
                child.print_node()


    def print_node_path(self,id):
        if self.root.find_node(id):
            print id + "/",
            self.root.find_node(id).print_parents()










