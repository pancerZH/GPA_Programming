# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calGPA(GPA, totalCredit, totalPoint, totalHundredPoint):
    """ 计算需要争取的优秀学分计算函数为
    (totalCredit * goal - totalPoint) / (5 - goal) """
    goalGPA = []
    result = []
    hundredResult = []
    for i in np.arange(GPA, 4.91, 0.01):
        x = (totalCredit * i - totalPoint) / (5 - i)
        goalGPA.append(round(i, 2))
        result.append(round(x, 1))
        hundredPoint = round(((totalHundredPoint + x * 95) / (totalCredit + x)), 1)
        hundredResult.append(hundredPoint)

    rawData = {'目标GPA': goalGPA, '需要的优秀学分': result, '百分制': hundredResult}
    dfResult = pd.DataFrame(rawData, columns=['目标GPA', '需要的优秀学分', '百分制'])
    dfResult.to_csv('goalGPA.csv')

    plt.plot(goalGPA, result)
    for i in zip(goalGPA, result, hundredResult):
        print('{}:\t{}\t{}'.format(i[0], i[1], i[2]))
    plt.show()


def main():
    file = pd.read_csv('GPA.csv')
    df = pd.DataFrame(file)

    totalCredit = float(df.sum(axis=0)[0])
    print('总学分=', totalCredit)
    totalPoint = df['学分'].mul(df['绩点']).sum(axis=0)
    GPA = round(totalPoint / totalCredit, 2)
    print('总绩点=', GPA)

    hundred = []
    for i in df['绩点']:
        if i == 5:
            hundred.append(95)
        elif i == 4:
            hundred.append(85)
        elif i == 3:
            hundred.append(75)
        elif i == 2:
            hundred.append(65)
        else:
            hundred.append(30)
    totalHundredPoint = df['学分'].mul(hundred).sum(axis=0)
    hundredPoint = round(totalHundredPoint / totalCredit, 1)
    print('百分制=', hundredPoint)

    calGPA(GPA, totalCredit, totalPoint, totalHundredPoint)


if __name__ == '__main__':
    main()