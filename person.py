class Person:
    OTHER = 0
    UNKNOWN = 1
    FEMALE = 2
    MALE = 3

    def __init__(self):
        self.fName = None
        self.lName = None
        self.DOB = -1
        self.DOD = -1
        self.gender = Person.UNKNOWN
        self.family = []
        # vars under this may not be necessary for person, move to family
        self.children = []
        self.parents = []
        self.siblings = []

    def editFName(self, fName):
        self.fName = fName

    def editLName(self, LName):
        self.lName = LName

    def setDOB(self, date):
        self.DOB = date

    def getDOB(self):
        return self.DOB
    
    def setDOD(self, date):
        self.DOD = date

    def getDOD(self):
        return self.DOD

    def setGender(self, gender):
        if gender not in (Person.OTHER, Person.UNKNOWN, Person.FEMALE, Person.MALE):
            print("Gender input is invalid")

        self.gender = gender

    def getGender(self):
        return self.gender

    def setChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def setParent(self, parent):
        self.parents.append(parent)

    def getParent(self):
        return self.parents

    def setsibling(self, sibling):
        self.siblings.append(sibling)

    def getsibling(self):
        return self.siblings

    # need to add remove
