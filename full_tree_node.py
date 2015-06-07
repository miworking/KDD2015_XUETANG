from access_log import *
from course_tree_node import *
import time,datetime

class FullTreeNode(object):
    def __init__(self,id):
        self.id = id
        self.children = {}
        self.category = None
        self.level = 0
        self.access_log = {}
        self.s = None
        self.earliest = None
        self.start = None




    def add_access_log(self,acess_record):
        access_time = datetime.datetime.strptime(acess_record.get_timestamp(),"%Y-%m-%dT%H:%M:%S")
        self.access_log[access_time] = (acess_record)

    def get_access_log(self):
        return self.access_log

    def set_level(self,level):
        self.level = level

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
            for i in range(self.level):
                print "--",
            print " >> " + timestamp + " from:" + record.source + ", event:" + record.event + " by :" + str(record.enrollment_id)


        for child in self.children.values():
            if child is not None:
                child.print_node_and_children()

    def print_node_and_children_to_file(self,output):
        print >>output,"|",
        for i in range(self.level):
            print >>output, "--",

        print >>output, "[" + str(self.id) + "] " + str(self.category) + " " + str(self.start) + ",earliest:" + str(self.earliest)

        for timestamp,record in self.access_log.items():
            print >>output,"|",
            for i in range(self.level):
                print >>output,"--",
            print  >>output," >> " + str(timestamp) + " from:" + record.source + ", event:" + record.event + " by :" + str(record.enrollment_id)


        for child in self.children.values():
            if child is not None:
                child.print_node_and_children_to_file(output)

    def get_earliest(self):
        self.update_earliest()
        return self.earliest

    def update_earliest(self):
        possible_earliest = datetime.datetime.now()
        if self.access_log :
            possible_earliest = min(self.access_log.keys())
        for child in self.children.values():
            if child.get_earliest() is not None:
                possible_earliest = min(possible_earliest,child.get_earliest())
        self.earliest = possible_earliest

    def rectify_time(self,time):
        print "start:" + str(self.start)
        print "earliest:" + str(self.earliest)
        if (self.start is None) & (self.earliest is None):
            self.start = time
        else:
            if (self.start is None):
                self.start = self.earliest
            elif self.start > self.earliest:
                self.start = self.earliest

        for child in self.children.values():
            child.rectify_time(self.start)

