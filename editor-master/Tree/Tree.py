# That file was generated automatically with DSL editor
# The moment of generation: 03/04/2022 01:09:01


class Tree:

    #VARS
    def __init__(self):
        self.entryTreeFlag = False
        self.exitTreeFlag = False
        self.tree = ""
        self.node = ""
        self.link = ""
        self.__state__ = "entry"

    #INNER
    #PROVIDED
    def entryTree(self):
        # TODO: add implementation
        pass

    def ifExitTree(self):
        # TODO: add implementation
        pass

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if entryTreeFlag:
                    node = nextNode(tree)
                    self.__state__ = "start_node"
                    continue
            if self.__state__ == "start_node" :
                if True:
                    node.entryNode()
                    self.__state__ = "end_node"
                    continue
            if self.__state__ == "end_node" :
                if node.ifExitNode():
                    self.__state__ = "get_link"
                    continue
            if self.__state__ == "get_link" :
                if True:
                    link = nextLink(tree)
                    self.__state__ = "check_link"
                    continue
            if self.__state__ == "check_link" :
                if link!="":
                    link.entryLink()
                    self.__state__ = "end_link"
                    continue
                popNodesStack()
                self.__state__ = "end_tree"
                continue
            if self.__state__ == "end_link" :
                if link.ifExitLink():
                    self.__state__ = "get_link"
                    continue
            if self.__state__ == "end_tree" :
                if True:
                    exitTreeFlag = True
                    self.__state__ = "exit"
                    continue


class Node:

    #VARS
    def __init__(self):
        self.entryNodeFlag = False
        self.exitNodeFlag = False
        self.node = ""
        self.__state__ = "entry"

    #INNER
    def __printNode(self):
        # TODO: add implementation
        pass

    def __printLink(self, link):
        # TODO: add implementation
        pass

    #PROVIDED
    def entryNode(self):
        # TODO: add implementation
        pass

    def ifExitNode(self):
        # TODO: add implementation
        pass

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if entryNodeFlag:
                    pushNodesStack(node)
                    self.__state__ = "print_node"
                    continue
            if self.__state__ == "print_node" :
                if True:
                    self.__printNode()
                    self.__state__ = "check_link"
                    continue
            if self.__state__ == "check_link" :
                if sizeNodesStack()>1:
                    self.__printLink(popLinkStack())
                    self.__state__ = "end_node"
                    continue
                exitNodeFlag = True
                self.__state__ = "exit"
                continue
            if self.__state__ == "end_node" :
                if True:
                    exitNodeFlag = True
                    self.__state__ = "exit"
                    continue


class Link:

    #VARS
    def __init__(self):
        self.entryLinkFlag = False
        self.exitLinkFlag = False
        self.link = ""
        self.tree = ""
        self.__state__ = "entry"

    #INNER
    #PROVIDED
    def entryLink(self):
        # TODO: add implementation
        pass

    def ifExitLink(self):
        # TODO: add implementation
        pass

    def run(self):
        while (True):
            if self.__state__ == "exit":
                break
            if self.__state__ == "entry" :
                if entryLinkFlag:
                    pushLinkStack(link)
                    self.__state__ = "get_tree"
                    continue
            if self.__state__ == "get_tree" :
                if True:
                    tree = nextTree(link)
                    self.__state__ = "start_tree"
                    continue
            if self.__state__ == "start_tree" :
                if True:
                    tree.entryTree()
                    self.__state__ = "end_tree"
                    continue
            if self.__state__ == "end_tree" :
                if tree.ifExitTree():
                    exitLinkFlag = True
                    self.__state__ = "exit"
                    continue


