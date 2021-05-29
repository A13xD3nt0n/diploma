import math

nodes = list()
rods = list()
loads = list()


def getNode(number):
    for node in nodes:
        print(type(node.toList()))
        if number == node.number:
            return node.toList()


class Node:
    def __init__(self, number, x, z, x_connection, z_connection):
        self._mNumber = number
        self._mX = x
        self._mZ = z
        self._mX_connection = x_connection
        self._mZ_connection = z_connection

    @property
    def x(self):
        return self._mX

    @property
    def number(self):
        return self._mNumber

    @property
    def z(self):
        return self._mZ

    @property
    def x_connection(self):
        return self._mX_connection

    @property
    def z_connection(self):
        return self._mZ_connection

    def toList(self):
        return [self.x, self.z, self.x_connection, self.z_connection]

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
        print(second_node)
        self._mL = math.pow(self._mSecond_node.z - self._mFirst_node.z,
                            2) + math.pow(self._mSecond_node.x -
                                          self._mFirst_node.x, 2)
        print('tyt3')
        self._mSin = (self._mSecond_node.z - self._mFirst_node.z) / \
                     self._mL
        self._mCos = (self._mSecond_node.x - self._mFirst_node.x) / \
                     self._mL

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

    def toList(self):
        return [self.first_node.number, self.second_node.number]

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
    def __init__(self, number, x, z):
        self._mNumber = number
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

    # @x.setter
    # def x(self, value):
    #     self._mX = value
    #
    # @z.setter
    # def z(self, value):
    #     self._mZ = value


class MathClass():
    def __init__(self, diag, matrix):
        self._mDiag = diag
        self._mMatrix = matrix

    @property
    def diag(self):
        return self._mDiag

    @property
    def matrix(self):
        return self._mMatrix
