class Family:
    UNKNOWN = 0
    MARRIED = 1
    SEPARATED = 2
    WIDOW = 3

    def __init__(self):
        self.father = None
        self.Mother = None
        self.children = []
        self.siblings = []
        self.relatType = -1
        self.completed = -1 #completed is 0. not completed is -1

    def parentRelat(self, type):
        if type not in (Family.UNKNOWN, Family.WIDOW, Family.SEPARATED, Family.MARRIED):
            print("invalid relationship type")
        self.relatType = type

    def setChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def setMother(self, parent):
        self.parents.append(parent)

    def getMother(self):
        return self.parents

    def setFather(self, parent):
        self.parents.append(parent)

    def getFather(self):
        return self.parents

    def setsibling(self, sibling):
        self.siblings.append(sibling)

    def getsibling(self):
        return self.siblings