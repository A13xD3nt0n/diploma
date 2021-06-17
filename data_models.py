import math
import math_algoritghm

nodes = list()
rods = list()
loads = list()
results = list()


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
    def __init__(self, number, first_node, second_node, EI):
        self._mNumber = number
        self._mFirst_node = first_node
        self._mSecond_node = second_node
        self._mEI = EI
        self._mL = math.sqrt(
            math.pow((self._mSecond_node.y - self._mFirst_node.y),
                     2) + math.pow((self._mSecond_node.x -
                                    self._mFirst_node.x), 2))
        self._mSin = (self._mSecond_node.y - self._mFirst_node.y) / \
                     self._mL
        self._mCos = (self._mSecond_node.x - self._mFirst_node.x) / \
                     self._mL
        C2 = self._mEI * self.cos_squared() / self._mL
        S2 = self._mEI * self.sin_squared() / self._mL
        CS = self._mEI * self.getSinCos() / self._mL
        self._mSeparate_matrix = [[C2, CS, -C2, -CS], [CS, S2, -CS, -S2],
                                  [-C2, -CS, C2, CS], [-CS, -S2, CS, S2]]

    @property
    def EI(self):
        return self._mEI

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
        return [self.first_node.number, self.second_node.number, self._mEI]

    def toShow(self):
        return [self.l, self.cos, self.sin, self.cos_squared(),
                self.sin_squared(), self.getSinCos()]

    @property
    def name(self):
        return str(self._mNumber) + 'й элемент [' + str(
            self._mFirst_node.number) + ':' + str(
            self._mSecond_node.number) + ']'

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
    def __init__(self, number, node, x, y):
        self._mNumber = number
        self._mNode = node
        self._mX = x
        self._mY = y

    @property
    def x(self):
        return self._mX

    @property
    def y(self):
        return self._mY

    @property
    def number(self):
        return self._mNumber

    @property
    def node(self):
        return self._mNode

    def toList(self):
        return [self._mNode.number, self.x, self.y]

    # @x.setter
    # def x(self, value):
    #     self._mX = value
    #
    # @z.setter
    # def z(self, value):
    #     self._mZ = value


class MathClass:
    def __init__(self, nodes, rods, loads):
        self._mMatrix = list()
        self._mMotions = list()
        self._mPillarReaction = list()
        self._mEfforts = list()
        self._mLoads = list()
        self._mPillarColumns = list()
        states = nodes.__len__() * 2

        # Построение общей матрицы жесткости
        for i in range(states):
            zero_list = [0] * states
            self._mMatrix.append(zero_list)
        for rod in rods:
            separate_matrix = rod.separate_matrix
            f_node = rod.first_node.number - 1
            s_node = rod.second_node.number - 1
            diff = s_node - f_node
            f_node = f_node * 2
            for i in range(2):
                for j in range(2):
                    self._mMatrix[i + f_node][j + f_node] += separate_matrix[i][
                        j]
                    self._mMatrix[i + f_node + diff * 2][
                        j + f_node + diff * 2] += \
                        separate_matrix[2 + i][
                            2 + j]
                    self._mMatrix[i + f_node + diff * 2][j + f_node] += \
                        separate_matrix[i + 2][j]
                    self._mMatrix[i + f_node][j + f_node + diff * 2] += \
                        separate_matrix[i][j + 2]

        # Учет опорных связей
        for node in nodes:
            number = node.number - 1
            if node.x_connection:
                self._mMatrix[number * 2][number * 2] = math.pow(10, 14)
            if node.y_connection:
                self._mMatrix[number * 2 + 1][number * 2 + 1] = math.pow(10, 14)

        # Преобразование нагружений
        for load in loads:
            new_load = [0] * states
            number = load.node.number - 1
            new_load[number * 2] = load.x
            new_load[number * 2 + 1] = load.y
            self._mLoads.append(new_load)

        # Формирование компактной формы матрицы жесткости
        compact_matrix = list()
        diag = list()
        for i in range(states):
            diag.append(compact_matrix.__len__() + 1)
            buffer_matrix = list()
            for j in range(i, -1, -1):
                buffer_matrix.append(self._mMatrix[j][i])
            k = buffer_matrix.__len__() - 1
            while buffer_matrix[k] == 0:
                buffer_matrix.pop(k)
                k -= 1
            for j in range(buffer_matrix.__len__()):
                compact_matrix.append(buffer_matrix[j])
        diag.append(compact_matrix.__len__()+1)

        #Добавление одного нуля над диагональю
        for i in range(diag.__len__()-1):
            if diag[i+1]-diag[i]==1 and i!=0:
                compact_matrix.insert(diag[i], 0)
                for j in range(i+1,diag.__len__(),1):
                    diag[j] += 1
        self._mCompactMatrix =compact_matrix
        self._mDiag = diag

        #Расчет узловых перемещений
        for load in self.loads:
            result = math_algoritghm.gaus(states,
                                                 [None]+self._mCompactMatrix,
                                                 [None]+load,
                                                 [None]+self._mDiag, 1)
            self._mMotions.append(result)

        #Расчет u и v
        for load in self.loads:
            pass

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
        return self._mMotions

    @property
    def pillar_reactions(self):
        return self._mPillarReaction

    @property
    def inner_efforts(self):
        return self._mEfforts

    @property
    def loads(self):
        return self._mLoads


