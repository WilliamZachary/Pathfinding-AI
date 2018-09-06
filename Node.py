#Node
#Author Zach

class Node:

    def __init__(self, mountain,x,y):
        self.inGraph= False
        self.inClosed= False
        self.mountain= mountain
        self.mountNeighbor= False
        self.goal= False
        self.coordinate= [x,y]
        self.depth= 0
        self.duplicated= False

        #Requested Informations

        self.identifier= None
        self.operator= None
        self.expan= 0
        self.gcost= 0
        self.hcost= 0
        self.fcost= 0
        self.childrens= []
        self.parent= None

    def setExpansion(self, index):
        self.expan = index

    def getExpansion(self):
        return self.expan

    def setDuplicate(self, value):
        self.duplicated = value

    def isDuplicated(self):
        return self.duplicated

    def setIdentifier(self, identifier):
        self.identifier= identifier

    def getIdentifier(self):
        return self.identifier

    def setOperator(self, operator):
        self.operator= operator

    def getOperator(self):
        return self.operator

    def setDepth(self, depth):
        self.depth= depth

    def addChildren(self,children):
        self.childrens.append(children)

    def getChildrens(self):
        return self.childrens

    def getDepth(self):
        return self.depth

    def setParent(self, parent):
        self.parent= parent

    def getParent(self):
        return self.parent

    def designateGoal(self):
        self.goal= True

    def isMountain(self):
        return self.mountain

    def isGoal(self):
        return self.goal

    def designateMountNeighbor(self):
        self.mountNeighbor = True

    def isMountNeighbor(self):
        return self.mountNeighbor

    def closeNode(self):
        self.inClosed= True
        self.expan= 0

    def isClosed(self):
        return self.inClosed

    def getCoordinate(self):
        return self.coordinate

    def inGraphAlr(self):
        return self.inGraph

    def putInGraph(self):
        self.inGraph= True

    def getActual(self):
        return self.gcost

    def setActual(self, gcost):
        self.gcost= gcost
        self.fcost = self.hcost + self.gcost

    def setHeuristic(self, hcost):
        self.hcost= hcost
        self.fcost = self.hcost + self.gcost

    def getHValue(self):
        return self.hcost

    def getFValue(self):
        return self.fcost
