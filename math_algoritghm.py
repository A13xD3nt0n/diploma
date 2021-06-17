import math
import numpy
from openpyxl import load_workbook


def decise_numpy(A, R):
    result = numpy.linalg.solve(A, R)
    return result


def gaus(N, A, R, DIAG, IER):
    # IER = -1 - BЫПOЛHЯETCЯ TOЛЬKO TPEУГOЛЬHOE PAЗЛOЖEHИE MATPИЦЫ A
    # IER = 0 - OБPATHЫЙ XOД ПO ПPABЫM ЧACTЯM
    # IER = 1 - ПPЯMOЙ И OБPATHЫЙ XOД
    IGAUS = 0
    print('N='+str(N))
    print('A='+str(A))
    print('R='+str(R))
    print('DIAG='+str(DIAG))
    print('IER='+str(IER))
    if IER != 0:
        for I in range(1, N + 1):
            print('I = ' + str(I))
            KN = DIAG[I]  # Берется первый номер диагонального элемента
            KL = KN + 1  # Индекс следующего диагонального элемента
            KU = DIAG[I + 1] - 1  # индекс элемента перед диагональным
            KH = KU - KL  # если больше 0 нет элементов между диагональными
            print("KH = " + str(KH))
            if KH > 0:
                K = I - KH # Индекс элемента
                IC = 0
                KLT = KU
                print('CYCLE element')
                for J in range(1, KH + 1):
                    IC = IC + 1
                    KLT = KLT - 1
                    KI = DIAG[K]
                    NO = DIAG[K + 1] - KI - 1
                    if NO > 0:
                        K1 = min(IC, NO)
                        S = 0
                        KS = K
                        for L in range(1, K1 + 1):
                            KS = KS - 1
                            print(
                                'L=' + str(L) + ' KS=' + str(KS) + ' KI=' + str(
                                    KI) +
                                ' KLT=' + str(KLT))
                            S = S + A[KI + L] * A[KLT + L]
                        A[KLT] = A[KLT] - S
                        print('S='+str(S))
                        K = K + 1
            KK = I
            S = 0
            print('cycle diag')
            print('KL = ' + str(KL) + ' KU = ' + str(KU))
            for KK1 in range(KL, KU + 1):
                KK = KK - 1
                KKI = DIAG[KK]
                if A[KKI] == 0:
                    break
                C = A[KK1] / A[KKI]
                S = S + C * A[KK1]
                print('KK1='+str(KK1)+' KKI='+str(KKI)+' kk='+str(KK))
                A[KK1] = C
            A[KN] = A[KN] - S
            print('A['+str(KN)+']='+str(A[KN])+' S='+str(S))
            # TODO -10 degree
            if A[KN] < math.pow(10, -10):
                IGAUS = IGAUS + 1
                return
    print('ПРЯМОЙ И ОБРАТНЫЙ ХОД')
    if IER >= 0:
        for I in range(1, N + 1):
            print('Ir='+str(I))
            KL = DIAG[I] + 1
            KU = DIAG[I + 1] - 1
            print('KU='+str(KU)+' KL='+str(KL))
            if KU >= KL:
                K = I
                S = 0
                for K1 in range(KL, KU + 1):
                    K = K - 1
                    S = S + A[K1] * R[K]
                    print('K1='+str(K1)+' K='+str(K)+' vektor R')
                R[I] = R[I] - S
                print('R['+str(I)+']='+str(R[I]))
        for I in range(1, N + 1):
            print('Iobr='+str(I))
            K = DIAG[I]
            R[I] = R[I] / A[K]
        N1 = N
        for L in range(1, N + 1):
            if L < N:
                KL = DIAG[N1] + 1
                KU = DIAG[N1 + 1] - 1
                if KU >= KL:
                    K = N1
                    for K1 in range(KL, KU + 1):
                        K = K - 1
                        R[K] = R[K] - A[K1] * R[N1]
                        print('R['+str(K)+']='+str(R[K]))
                N1 = N1 - 1
    return R


if __name__ == '__main__':
    N = 8
    A = [None, math.pow(10, 14),
         math.pow(10, 14), 9.6,
         50, 0, -25,
         33.333333, 0,
         37.8, 0, -25,
         math.pow(10, 14), -9.6,
         25.6, 9.6, -12.8, 0, 0, -9.6, -12.8,
         47.733333, 0, -7.2, 9.6, -33.333333, 0, -7.2, -9.6]
    R = [None, 0, 0, 0, -280, 0, 0, 0, 0]
    DIAG = [None, 1, 2, 4, 7, 9, 12, 14, 21, A.__len__()]
    # N = 8
    # A = [None, 100000000000000.0, 100000000000000.0, 9.6, 50.0, 0.0, -25.0,
    #      33.333333333333336, 0, 100000000000000.0, 0.0, -25.0, 7.2, -9.6,
    #      25.600000000000005, 9.6, -12.800000000000002, 0.0, 0.0, -9.6,
    #      -12.800000000000002, 47.733333333333334, 0.0, -7.2, 9.6,
    #      -33.333333333333336, 0.0, -7.2, -9.6]
    # R = [None, 0, 0, 0, -280, 0, 0, 0, 0]
    # DIAG = [None, 1, 2, 4, 7, 9, 12, 14, 21, 29]
    # IER = 1
    # R = [None, 0, 1, 0, 0, 0]
    # A = [None, 2, 3, -2, 5, -2, 10, -3, 10, 4, 0, 0, -1]
    # DIAG = [None, 1, 2, 4, 6, 8, A.__len__()]
    # N = 5
    # N = 8
    # A = [None, math.pow(10,18), 320, 96,   math.pow(10,18) ,-96,-38.4,
    #      2320, 654,  160,  96.,math.pow(10,18), -750, -375,  6000, 750, 1000,
    #      750,    750, -1500, -750,4000, -1500, 2000, 1500 ]
    # R = [None, 222, 25,   444,  50,  666,    40,   64,  38]
    # DIAG = [None, 1,2,4,7,11,14,18,21,25]
    print('A=' + str(A) + ' R=' + str(R) + ' DIAG=' + str(DIAG))
    result = gaus(N=N,
                  A=A,
                  R=R,
                  DIAG=DIAG,
                  IER=1)
    # wb = load_workbook('./123.xlsx')
    #
    # sheet = wb['Матрица жесткости']
    # cell_range = sheet['S19':'Z26']
    # A = list()
    # for row in cell_range:
    #     input = [r.value for r in row]
    #     A.append(input)
    # A[0][0] = math.pow(10,14)
    # A[1][1] = math.pow(10,14)
    # A[5][5] = math.pow(10,14)
    # cell_range = sheet['M24':'M31']
    # R = list()
    # for row in cell_range:
    #     input = [r.value for r in row]
    #     R.append(input)
    # print('Вектор Z1: ' +str(decise_numpy(A,R)))
    # cell_range = sheet['O24':'O31']
    # R = list()
    # for row in cell_range:
    #     input = [r.value for r in row]
    #     R.append(input)
    # print('Вектор Z2: ' + str(decise_numpy(A, R)))
    print('R = ' + str(result))
