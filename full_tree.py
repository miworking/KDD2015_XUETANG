from course_tree import *
from full_tree_node import *
from access_log import *
import pickle
import io
import pandas as pd

class FullTree(object):

    def __init__(self):
        self.course_id = None
        self.root = FullTreeNode(0)
        self.seq = {}
        self.video = {}
        self.problems = {}

    def __init__(self,course_tree,course_id):
        self.course_id = course_id
        self.root = course_tree.root.copy_to_FullNode()
        self.seq = {}
        self.video = {}
        self.problems = {}



    def get_root(self):
        return self.root

    def add_access_log(self,access_record):
        node = self.root.find_node(access_record.get_id())
        if node is None:
            node = FullTreeNode(access_record.get_id())
            node.set_level(1)
            node.category = 'unknown'
            node.start = None
            self.root.children[access_record.get_id()] = node
        node.add_access_log(access_record)

    def print_tree(self):
        print "=======================================" + str(self.course_id)
        for id,child in self.root.children.items():
            if child is None:
                print '(' + id + ')'
            else:
                child.print_node_and_children()


    def print_tree_to_file(self,output):
        print >>output,"=======================================" + str(self.course_id)
        for id,child in self.root.children.items():
            if child is None:
                print >>output,'(' + id + ')'
            else:
                child.print_node_and_children_to_file(output)

    def  rectify_time(self):
        self.root.rectify_time(self.root.get_earliest())


    def add_insula_to_sequentials(self):
        self.update_seq()
        for id,child in self.root.get_children().items():
            if child.get_category() == "unknown":
                parent_seq = self.find_nearest_seq(child.get_start())
                if parent_seq is not None:
                    parent_seq.get_children()[id] = child
                    child.adjust_category()
                    child.set_level(4)
                    del self.root.children[id]




    def update_seq(self):
        self.root.find_seq(self.seq)

    def print_seq(self):
        keys = self.seq.keys()
        keys.sort()
        for key in keys:
            print str(key)+ " : " + str(self.seq[key].get_id())


    def find_nearest_seq(self,time):
        self.update_seq()
        keys = self.seq.keys()
        keys.sort()
        last = None
        nearest = self.root
        for timestamp in keys:
            if timestamp > time:
                if last is None:
                    return None
                else:
                    nearest = self.seq[last]
                    break
            last = timestamp
        return nearest



    def update_video(self):
        self.root.find_video(self.video)

    def print_video(self):
        keys = self.video.keys()
        keys.sort()
        for key in keys:
            print str(key)+ " : " + str(self.video[key].get_id())

    def update_video(self):
        self.root.find_video(self.video)

    def print_video(self):
        print "=============videos:=============="
        keys = self.video.keys()
        keys.sort()
        for key in keys:
            print str(key)+ " : " + str(self.video[key].get_id())

    def update_problems(self):
        self.root.find_problems(self.problems)

    def print_problems(self):
        print "=============problems:=============="
        keys = self.problems.keys()
        keys.sort()
        for key in keys:
            print str(key)+ " : " + str(self.problems[key].get_id())


    def update(self):
        self.rectify_time()

        self.add_insula_to_sequentials()
        self.update_video()
        # self.print_video()
        path = './train/courseDump/' + self.course_id +  '.txt'

        self.update_problems()
        # self.print_problems()
        self.update_sequentialID()
        self.update_chapterID()



        f = open(path,'wb')
        pickle.dump(self,f,1)
        f.close()
        print "pickled to " + path

        path2 = './train/fullTree/' + self.course_id + '.txt'
        output = open(path2,'wb')
        self.print_tree_to_file(output)
        output.close()
        print "printed to " + path2

        modules=pd.DataFrame(columns=['module_id','start','category','sequentialId','chapterId'])
        get_time = lambda  x : x.find('.')

        self.get_module_matrix(modules)
        path3 = './train/fullTree/' + self.course_id + "_moduleIDs.csv"
        modules.to_csv(path3,index=False,index_label=False,header=1,encoding='ascii')
        print "modules are printed to " + str(path3)

    def get_module_matrix(self,matrix):
        self.root.add_modules(matrix)

    def get_video_visite_times(self,enrollment_id):
        sum_visit = 0;
        for vd in self.video.values():
            if vd.visited(enrollment_id):
                sum_visit += 1
        return sum_visit

    def get_problems_visite_times(self,enrollment_id):
        sum_visit = 0;
        for vd in self.problems.values():
            if vd.visited(enrollment_id):
                sum_visit += 1
        return sum_visit

    def update_sequentialID(self):
        self.root.set_sequentialID(None)

    def update_chapterID(self):
        self.root.set_chapterID(None)








