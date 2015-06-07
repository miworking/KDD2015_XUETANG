from access_log import *
from course_tree_node import *

class Enrollment_Tree_Node(object):
    def __init__(self,id):
        self.id = id
        self.children = {}
        self.category = None
        self.level = 0
        self.access_log = {}
        self.start = None




    def add_access_log(self,acess_record):
        self.access_log[acess_record.get_timestamp()] = acess_record

    def get_access_log(self):
        return self.access_log

    def set_level(self,level):
        self.level = level

    def get_children(self):
        return self.children

    def get_id(self):
        return self.id

    def get_category(self):
        return self.category

    def find_node(self,id):
        if self is None:
            return None
        if self.id == id:
            return self
        else:
            for child_id,child in self.children.items():
                if child is not None:
                    if child.find_node(id) is not None:
                        return child.find_node(id)
        return None

    def print_node_and_children(self):
        print "|",
        for i in range(self.level):
            print "--",
        print "[" + str(self.id) + "] " + str(self.category) + " " + str(self.start)


        for timestamp,record in self.access_log.items():
            print "|",
            for i in range(self.level):
                print "--",
            print " >> " + timestamp + " from:" + record.source + ", event:" + record.event


        for child in self.children.values():
            if child is not None:
                child.print_node_and_children()