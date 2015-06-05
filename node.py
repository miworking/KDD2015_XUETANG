from tree import *

class Node(object):
    def __init__ (self,id,parent,children,level,category) :
        self.id = id
        self.parent = parent
        self.children = children
        self.level = level
        self.category = category

    def __init__ (self, id) :
        self.id = id
        self.parent = None
        self.children = {}
        self.level = 0
        self.category = None




    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_level(self):
        return self.level

    def set_level(self,level):
        self.level = level
        for child in self.get_children().values():
            if child is not None:
                child.set_level(level + 1)


    def has_leaf(self,Node):
        return True

    def get_id(self):
        return self.id

    def level_plus(self):
        self.level += 1
        for child in self.get_children().values():
            if child is not None:
                child.level_plus()









    def find_node(self,id):
        if self.id == id:
            return self.parent
        else:
            for child_id,child in self.children.items():
                if child_id == id:
                    return self
                else:
                    if child is not None:
                        if child.find_node(id) is not None:
                            return child.find_node(id)
        return None




    def insert(self,node):
        for key,value in self.children.items():
            if node.get_id() == key:
                self.children[key] = node
                node.level = self.level + 1
                node.parent = self
                # print "[" + str(node.get_level()) + "]" + key + " to :" + self.id
                return True
            else:
                if value is not None:
                    if value.insert(node):
                        return True
        return False

    def print_node(self):
        print "|",
        for i in range(self.level):
            print "----",
        print "[" + self.id + "]"

        for child in self.children.values():
            if child is not None:
                child.print_node()


    def get_first_level(self):
        if self.level == 1:
            return self
        else:
            return self.parent.get_first_level()


    def print_parents(self):
        if self.parent is None:
            return
        else :
            print self.id + " /",
            self.parent.print_parents()



    def print_weird(self):
        if self.children is not None:
            for cid,child in self.children.items():
                if child is None:
                    print cid
                else:
                    child.print_weird()



