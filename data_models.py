import math
import math_algoritghm

nodes = list()
rods = list()
loads = list()



class Node:
    def __init__(self, number, x, y, x_connection, y_connection):
        self._mNumber = number
        self._mX = x
        self._mY = y
        self._mX_connection = x_connection
        self._mY_connection = y_connection
        self._mX_load = 0
        self._mY_load = 0

    @property
    def x(self):
        return self._mX

    @property
    def number(self):
        return self._mNumber

    @property
    def y(self):
        return self._mY

    @property
    def x_connection(self):
        return self._mX_connection

    @property
    def y_connection(self):
        return self._mY_connection

    @property
    def x_load(self):
        return self._mX_load

    @property
    def y_load(self):
        return self._mY_load

    @x_load.setter
    def x_load(self, value):
        self._mX_load = value

    @y_load.setter
    def y_load(self, value):
        self._mY_load = value

    def toList(self):
        return [self.x, self.y, self.x_connection, self.y_connection]

    #
    # @x.setter
    # def x(self, value):
    #     self._mX = value
    #
    # @z.setter
    # def z(self, value):
    #     self._mZ = value
    #
    # @z_connection.setter
    # def z_connection(self, value):
    #     self._mZ_connection = value
    #
    # @x_connection.setter
    # def x_connection(self, value):
    #     self._mX_connection = value
    #
    # @number.setter
    # def number(self, value):
    #     self._mNumber = value


class Rod:
    def __init__(self, number, first_node, second_node):
        self._mNumber = number
        self._mFirst_node = first_node
        self._mSecond_node = second_node
        self._mL = math.sqrt(math.pow((self._mSecond_node.y - self._mFirst_node.y),
                            2) + math.pow((self._mSecond_node.x -
                                          self._mFirst_node.x), 2))
        self._mSin = (self._mSecond_node.y - self._mFirst_node.y) / \
                     self._mL
        self._mCos = (self._mSecond_node.x - self._mFirst_node.x) / \
                     self._mL
        C2 = self.cos_squared()
        S2 = self.sin_squared()
        CS = self.getSinCos()
        self._mSeparate_matrix = [[C2, CS, -C2, -CS], [CS, S2, -CS, -S2],
                                  [-C2, -CS, C2, CS], [-CS, -S2, CS, S2]]


    @property
    def first_node(self):
        return self._mFirst_node

    @property
    def second_node(self):
        return self._mSecond_node

    @property
    def cos(self):
        return self._mCos

    @property
    def sin(self):
        return self._mSin

    @property
    def number(self):
        return self._mNumber

    @property
    def l(self):
        return self._mL

    @property
    def separate_matrix(self):
        return self._mSeparate_matrix

    def toList(self):
        return [self.first_node.number, self.second_node.number]

    def toShow(self):
        return [self.l, self.cos, self.sin, self.cos_squared(),
                self.sin_squared(), self.getSinCos()]

    @property
    def name(self):
        return str(self._mNumber)+'й элемент ['+str(
            self._mFirst_node.number)+':'+str(self._mSecond_node.number)+']'


    # @first_node.setter
    # def x(self, value):
    #     self._mFirst_node = value
    #     self._mSin = (self._mSecond_node.z - self._mFirst_node.z) / \
    #                  (self.sin_squared() + self.cos_squared())
    #     self._mCos = (self._mSecond_node.x - self._mFirst_node.x) / \
    #                  (self.sin_squared() + self.cos_squared())
    #
    # @second_node.setter
    # def z(self, value):
    #     self._mSecond_node = value
    #     self._mSin = (self._mSecond_node.z - self._mFirst_node.z) / \
    #                  (self.sin_squared() + self.cos_squared())
    #     self._mCos = (self._mSecond_node.x - self._mFirst_node.x) / \
    #                  (self.sin_squared() + self.cos_squared())

    def getSinCos(self):
        return self._mCos * self._mSin

    def cos_squared(self):
        return self._mCos * self._mCos

    def sin_squared(self):
        return self._mSin * self._mSin


class Load:
    def __init__(self, number, node, x, z):
        self._mNumber = number
        self._mNode = node
        self._mX = x
        self._mZ = z

    @property
    def x(self):
        return self._mX

    @property
    def z(self):
        return self._mZ

    @property
    def number(self):
        return self._mNumber

    @property
    def node(self):
        return self._mNode

    def toList(self):
        return [self.number, self.x, self.z]

    # @x.setter
    # def x(self, value):
    #     self._mX = value
    #
    # @z.setter
    # def z(self, value):
    #     self._mZ = value


class MathClass:
    def __init__(self, nodes, rods, loads):
        self._mDiag = list()
        self._mMatrix = list()
        self._mCompactMatrix = list()
        self._mMotion = list()
        self._mPillarReaction = list()
        self._mEfforts = list()
        self._mLoad = list()
        states = nodes.__len__() * 2
        for i in range(states):
            zero_list = [0] * states
            self._mMatrix.append(zero_list)

        self._mMotion = math_algoritghm.gaus(states, self._mCompactMatrix, )


    @property
    def diag(self):
        return self._mDiag

    @property
    def matrix(self):
        return self._mMatrix

    @property
    def compact_matrix(self):
        return self._mCompactMatrix

    @property
    def motions(self):
        return self._mMotion

    @property
    def pillar_reactions(self):
        return self._mPillarReaction

    @property
    def inner_efforts(self):
        return self._mEfforts

    @property
    def loads(self):
        return [None] + self._mLoad