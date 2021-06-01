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
    igaus = 0
    if IER != 0:
        for i in range(1, N + 1):
            print('I = ' + str(i))
            kn = DIAG[i]  # Берется первый номер диагонального элемента
            kl = kn + 1  # Индекс следующего матрицы элемента
            ku = DIAG[i + 1] - 1  # 3-1=2
            kh = ku - kl  # 2-2=0
            print("KH = " + str(kh))
            if kh > 0:
                k = i - kh
                ic = 0
                klt = ku
                print('CYCLE element')
                for j in range(1, kh + 1):
                    ic = ic + 1
                    klt = klt - 1
                    ki = DIAG[k]
                    no = DIAG[k + 1] - ki - 1
                    if no > 0:
                        k1 = min(ic, no)
                        s = 0
                        ks = k
                        for l in range(1, k1 + 1):
                            ks = ks - 1
                            print(
                                'L=' + str(l) + ' KS=' + str(ks) + ' ki=' + str(
                                    ki) +
                                ' klt=' + str(klt))
                            s = s + A[ki + l] * A[klt + l]
                        A[klt] = A[klt] - s
                        k = k + 1
            kk = i
            s = 0
            print('cycle diag')
            print('kl = ' + str(kl) + ' ku = ' + str(ku))
            for kk1 in range(kl, ku + 1):
                kk = kk - 1
                kki = DIAG[kk]
                if A[kki] == 0:
                    break
                c = A[kk1] / A[kki]
                s = s + c * A[kk1]
                A[kk1] = c
            A[kn] = A[kn] - s
            # TODO -10 degree
            if A[kn] < math.pow(1, -10):
                igaus = igaus + 1
                return
    if IER < 0:
        return
    print('ПРЯМОЙ И ОБРАТНЫЙ ХОД')
    if IER >= 0:
        for i in range(1, N + 1):
            kl = DIAG[i] + 1
            ku = DIAG[i + 1] - 1
            if ku < kl:
                k = i
                s = 0
                for k1 in range(kl, ku + 1):
                    k = k - 1
                    s = s + A[k1] * R[k]
                R[i] = R[i] - s
        for i in range(1, N + 1):
            k = DIAG[i]
            R[i] = R[i] / A[k]
        n1 = N
        for l in range(1, N + 1):
            if l >= N:
                kl = DIAG[i] + 1
                ku = DIAG[i + 1] - 1
                if ku < kl:
                    k = n1
                    for k1 in range(kl, ku + 1):
                        k = k - 1
                        R[k] = R[k] - A[k1] * R[n1]
            n1 = n1 - 1
    return R


if __name__ == '__main__':
    N = 8,
    A = [None, math.pow(10, 14),
         math.pow(10, 14), 9.6,
         50, 0, -25,
         33.33,
         37.8, 0, -25,
         math.pow(10, 14), -9.6,
         25.6, 9.6, -12.8, 0, 0, -9.6, -12.8,
         47.73, 0, -7.2, 9.6, -33.33, 0, -7.2, -9.6],
    R = [None, 0, 0, 0, -280, 0, 0, 0, 0],
    DIAG = [None, 1, 2, 4, 7, 8, 11, 13, 20, len(A)],
    IER = 1
    result = gaus(N=8,
                  A=[None, math.pow(10, 14),
                     math.pow(10, 14), 9.6,
                     50, 0, -25,
                     33.33,
                     37.8, 0, -25,
                     math.pow(10, 14), -9.6,
                     25.6, 9.6, -12.8, 0, 0, -9.6, -12.8,
                     47.73, 0, -7.2, 9.6, -33.33, 0, -7.2, -9.6],
                  R=[None, 0, 0, 0, -280, 0, 0, 0, 0],
                  DIAG=[None, 1, 2, 4, 7, 8, 11, 13, 20, len(A)],
                  IER=1)
    # wb = load_workbook('./123.xlsx')
    #
    # sheet = wb['Матрица жесткости']
    # cell_range = sheet['S19':'Z26']
    # A = list()
    # for row in cell_range:
    #     input = [r.value for r in row]
    #     A.append(input)
    # print(A)
    # A[0][0] = math.pow(10,14)
    # A[1][1] = math.pow(10,14)
    # A[5][5] = math.pow(10,14)
    # print(A)
    # cell_range = sheet['M24':'M31']
    # R = list()
    # for row in cell_range:
    #     input = [r.value for r in row]
    #     R.append(input)
    # print(R)
    print('R = ' + str(result))
