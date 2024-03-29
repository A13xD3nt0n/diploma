import math
import math_algoritghm
import time
import sys
import json

nodes = list()
rods = list()
loads = list()


class InputData:
    nodes = list()
    rods = list()
    loads = list()

    @staticmethod
    def add_node(x, y, x_connection,
                 y_connection):
        number = len(nodes) + 1
        nodes.append(Node(number, x, y, x_connection, y_connection))

    @staticmethod
    def add_rod(first_node_number, second_node_number, EI):
        number = len(rods) + 1
        rods.append(Rod(number, nodes[first_node_number - 1], nodes[
            second_node_number - 1], EI))

    @staticmethod
    def add_load(node, x, y):
        number = len(loads) + 1
        loads.append(Load(number, node, x, y))

    @staticmethod
    def load_input_data():
        pass

    @staticmethod
    def is_ready():
        return True if len(loads) != 0 and len(rods) != 0 and len(nodes) != 0 \
            else False


class Node:
    def __init__(self, number, x, y, x_connection, y_connection):
        self._mNumber = number
        self._mX = x
        self._mY = y
        self._mX_connection = x_connection
        self._mY_connection = y_connection

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

    def toList(self):
        return [str(self.x), str(self.y), 'Есть' if self.x_connection else '',
                'Есть' if self.y_connection else '']


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
        print(self._mFirst_node.x)
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
        return [str(self.first_node.number), str(self.second_node.number),
                str(self._mEI)]

    def toShow(self):
        return ['{:.3f}'.format(self.l), '{:.3f}'.format(self.cos),
                '{:.3f}'.format(self.sin),
                '{:.3f}'.format(self.cos_squared()),
                '{:.3f}'.format(self.sin_squared()),
                '{:.3f}'.format(self.getSinCos())]

    @property
    def name(self):
        return str(self._mNumber) + 'й элемент [' + str(
            self._mFirst_node.number) + ':' + str(
            self._mSecond_node.number) + ']'

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
        return [str(self._mNode.number), str(self.x), str(self.y)]


class MathClass:
    def __init__(self, nodes, rods, loads):
        self._mMatrix = list()
        self._mMotions = list()
        self._mPillarReaction = list()
        self._mEfforts = list()
        self._mLoads = list()
        self._mPillarColumns = list()
        self._mPillarColumnsNames = list()
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
            buffer = list()
            number = node.number - 1
            if node.x_connection:
                for i in range(states):
                    buffer.append(self._mMatrix[i][number * 2])
                self._mPillarColumns.append(buffer)
                self._mMatrix[number * 2][number * 2] = math.pow(10, 14)
                self._mPillarColumnsNames.append('X' + str(number + 1))
            buffer = list()
            if node.y_connection:
                for i in range(states):
                    buffer.append(self._mMatrix[i][number * 2 + 1])
                self._mPillarColumns.append(buffer)
                self._mMatrix[number * 2 + 1][number * 2 + 1] = math.pow(10, 14)
                self._mPillarColumnsNames.append('Y' + str(number + 1))

        # Преобразование нагружений
        for load in loads:
            new_load = [0] * states
            number = load.node.number - 1
            new_load[number * 2] = load.x
            new_load[number * 2 + 1] = load.y
            self._mLoads.append(new_load)
        print(5)
        # Формирование компактной формы матрицы жесткости
        start_time = time.clock()
        compact_matrix = list()
        diag = list()
        for i in range(states):
            print(compact_matrix)
            print(self._mMatrix)
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
        diag.append(compact_matrix.__len__() + 1)
        print(6)
        # Добавление одного нуля над диагональю
        for i in range(diag.__len__() - 1):
            if diag[i + 1] - diag[i] == 1 and i != 0:
                compact_matrix.insert(diag[i], 0)
                for j in range(i + 1, diag.__len__(), 1):
                    diag[j] += 1
        self._mCompactMatrix = compact_matrix
        self._mDiag = diag
        print(7)
        # Расчет узловых перемещений
        for load in self.loads:
            result = math_algoritghm.gaus(states,
                                          [None] + self._mCompactMatrix,
                                          [None] + load,
                                          [None] + self._mDiag, 1)
            result.pop(0)
            self._mMotions.append(result)
        print('ВРЕМЯ РАСЧЕТА КОМПАКТНЫМ МЕТОДОМ:' + str(time.clock() -
                                                        start_time))
        start_time = time.clock()
        for load in self.loads:
            math_algoritghm.decise_numpy(self.matrix, load)
        print('ВРЕМЯ РАСЧЕТА ОБЫЧНЫМ МЕТОДОМ:' + str(time.clock() - start_time))
        # Опорные реакции
        for motion in self.motions:
            buffer = list()
            for pillar in self._mPillarColumns:
                summa = 0
                for i in range(states):
                    summa += pillar[i] * motion[i]
                buffer.append(summa)
            self._mPillarReaction.append(buffer)

        # Усилия в узлах
        for motion in self.motions:
            buffer = list()
            for rod in rods:
                f_node = rod.first_node.number - 1
                s_node = rod.second_node.number - 1
                effort = rod.EI * (((motion[s_node * 2] - motion[
                    f_node * 2])) * rod.cos + rod.sin * (
                                           motion[s_node * 2 + 1] - motion[
                                       f_node * 2 + 1])) / rod.l
                buffer.append(effort)
            self._mEfforts.append(buffer)

        # Исследование
        print('КОЛИЧЕСТВО СТЕПЕНЕЙ СВОБОДЫ:' + str(states))
        s = 0
        for strike in self.matrix:
            s += sys.getsizeof(strike)
        print('ОБЪЕМ ПАМЯТИ НЕКОМПАКТНОЙ ФОРМЫ:' + str(
            sys.getsizeof(self.matrix) + s))
        print('ОБЪЕМ ПАМЯТИ КОМПАКТНОЙ ФОРМЫ:' + str(sys.getsizeof(
            self.compact_matrix) + sys.getsizeof(self.diag)))

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

    @property
    def pillar_reactions_name(self):
        return self._mPillarColumnsNames

    def load_result_list(self, index):
        return {'L': self.loads[index], 'E': self.inner_efforts[index],
                'M': self.motions[index], 'PR': self.pillar_reactions[index],
                'PRN': self.pillar_reactions_name}
