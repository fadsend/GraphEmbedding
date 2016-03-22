from enum import Enum


class Type(Enum):
    Q_NODE = 1
    P_NODE = 2
    LEAF = 3


class Label(Enum):
    FULL = 1
    EMPTY = 2
    PERTINENT = 3


class PQnode(object):

    # TODO: should be extendend
    def __init__(self, nodeType, label):
        self.mType = nodeType
        self.mLabel = label

    def setType(self, newType):
        self.mType = newType

    def getType(self):
        return self.mType

    def setLabel(self, newLabel):
        self.mLabel = newLabel

    def getLabel(self):
        return self.mLabel
