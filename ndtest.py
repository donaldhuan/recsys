from numpy import *
from scipy.stats import *
from math import *

def numin(num1, num2, ls):
    a = 0
    if num2 != max(ls):
        for i in range(0, len(ls)):
            if ls[i] >= num1 and ls[i] < num2:
                a += 1
    else:
        for i in range(0, len(ls)):
            if ls[i] >= num1 and ls[i] <= num2:
                a += 1
    return a
    
def nd(result):
    result.sort()
    aver = average(result)
    l = len(result)
    b2 = 0
    for i in range(0, l):
        b2 += (result[i] - aver) ** 2
    b2 = b2 * 1.0 / l
    a = result[-1] - result[0]
    b = a * 1.0 / 10
    ls = []
    ls1 = []
    flag = []
    for i in range(0, 10):
        flag.append(0)
        if i != 9:
            num1 = result[0] + i * b
            num2 = num1 + b
        else:
            num1 = result[0] + 9 * b
            num2 = max(result)
        ls.append(numin(num1, num2, result))
        if ls[i] < 5:
            ls1.append((ls[i], 1))
        else:
            ls1.append((ls[i], 0))
        
    lss = []
    for i in range(0, 10):
        if flag[i] == 1:
            continue
        if ls1[i][1] == 1:
            x = ls1[i][0]
            if i == 9:
                x += lss[len(lss) - 1][0]
                y = lss[len(lss) - 1][1]
                z = lss[len(lss) - 1][2]
                lss.remove(lss[len(lss) - 1])
                lss.append((x, y, 9))
            for j in range(i + 1, 10):
                x += ls1[j][0]
                if x >= 5:
                    lss.append((x, i, j))
                    for p in range(i + 1, j + 1):
                        flag[p] = 1
                    break
                elif j == 9:
                    x += lss[len(lss) - 1][0]
                    y = lss[len(lss) - 1][1]
                    z = lss[len(lss) - 1][2]
                    lss.remove(lss[len(lss) - 1])
                    lss.append((x, y, 9))
                    for p in range(i + 1, j + 1):
                        flag[p] = 1
        else:
            lss.append(((ls1[i][0]), i, i))
    chi = 0
    b2 = sqrt(b2)
    print lss
    '''
    x = []
    y = []
    for i in range(0, len(lss)):
        x.append(result[0] + b * (lss[i][1] + lss[i][2]) * 1.0 / 2)
        y.append(lss[i][0])
    plot(x, y)
    show()
    '''
    for i in range(0, len(lss)):
        if lss[i][1] == lss[i][2] and lss[i][1] != len(ls1) - 1 and lss[i][1] != 0:
            chi += lss[i][0] ** 2 * 1.0 / (l * (norm.cdf((result[0] + (lss[i][1] + 1) * b - aver) * 1.0 / b2) - norm.cdf((result[0] + lss[i][1] * b - aver) * 1.0 / b2)))
        elif lss[i][1] == lss[i][2] and lss[i][1] == 0:
            chi += lss[i][0] ** 2 * 1.0 / (l * norm.cdf((result[0] + (lss[i][1] + 1) * b - aver) * 1.0 / b2))
        elif lss[i][1] == lss[i][2] and lss[i][1] == len(ls1) - 1:
            chi += lss[i][0] ** 2 * 1.0 / (l * (1 - norm.cdf((result[0] + lss[i][1] * b - aver) * 1.0 / b2)))
        elif lss[i][1] != lss[i][2] and lss[i][2] != len(ls1) - 1 and lss[i][1] != 0:
            chi += lss[i][0] ** 2 * 1.0 / (l * (norm.cdf((result[0] + (lss[i][2] + 1) * b - aver) * 1.0 / b2) - norm.cdf((result[0] + lss[i][1] * b -aver) * 1.0 / b2)))
        elif lss[i][1] != lss[i][2] and lss[i][1] == 0:
            chi += lss[i][0] ** 2 * 1.0 / (l * norm.cdf((result[0] + (lss[i][2] + 1) * b - aver) * 1.0 / b2))
        elif lss[i][1] != lss[i][2] and lss[i][2] == len(ls1) - 1:
            chi += lss[i][0] ** 2 * 1.0 / (l * (1 - norm.cdf((result[0] + lss[i][1] * b - aver) * 1.0 / b2)))
    chi -= l
    return chi2(len(lss) - 3).cdf(chi)

if __name__ == '__main__':
    from sys import argv
    f = open('result/result_%d' % int(argv[1]))
    import pickle
    print nd(pickle.load(f))

