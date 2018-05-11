# -*- coding:utf-8 -*-

from math import ceil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calGPA(GPA, totalCredit, totalPoint, totalHundredPoint):
    """ 计算需要争取的优秀学分计算函数为
    (totalCredit * goal - totalPoint) / (5 - goal) """
    goalGPA = []
    result = []
    hundredResult = []
    # 学分预测上界
    boundary = 4.8

    for i in np.arange(GPA, boundary, 0.01):
        # 避免需要的优秀学分一栏出现负数
        if totalCredit * i <= totalPoint:
            continue
        x = (totalCredit * i - totalPoint) / (5 - i)
        goalGPA.append(round(i, 2))
        # 需要的学分根据实际情况，向上取整到个位
        result.append(ceil(x))
        hundredPoint = round(((totalHundredPoint + x * 95) / (totalCredit + x)), 1)
        hundredResult.append(hundredPoint)

    rawData = {'Goal GPA': goalGPA, '"A" credits needed': result, 'GPA in 100': hundredResult}
    dfResult = pd.DataFrame(rawData, columns=['Goal GPA', '"A" credits needed', 'GPA in 100'])
    dfResult.to_csv('goal_GPA.csv')

    # 图表美化
    plt.plot(goalGPA, result, 'b*-')
    plt.title('Goal GPA and "A" Credits Needed')
    plt.xlabel('Goal GPA')
    plt.ylabel('"A" Credits Needed')
    # print('{}:\t{}\t{}'.format('目标GPA', '需要的优秀学分', '百分制'))
    # for i in zip(goalGPA, result, hundredResult):
        # print('{}:\t{}\t{}'.format(i[0], i[1], i[2]))
    
    # 四学期最好GPA预测
    # 每学期学分调整
    credits_for_each_sem = 24
    best_gpa_in_one_sem = (totalPoint + credits_for_each_sem * 1 * 5) / (totalCredit + credits_for_each_sem * 1)
    best_gpa_in_one_sem_100 = best_gpa_in_one_sem * 10 + 45
    best_gpa_in_two_sem = (totalPoint + credits_for_each_sem * 2 * 5) / (totalCredit + credits_for_each_sem * 2)
    best_gpa_in_two_sem_100 = best_gpa_in_two_sem * 10 + 45
    best_gpa_in_three_sem = (totalPoint + credits_for_each_sem * 3 * 5) / (totalCredit + credits_for_each_sem * 3)
    best_gpa_in_three_sem_100 = best_gpa_in_three_sem * 10 + 45
    best_gpa_in_four_sem = (totalPoint + credits_for_each_sem * 4 * 5) / (totalCredit + credits_for_each_sem * 4)
    best_gpa_in_four_sem_100 = best_gpa_in_four_sem * 10 + 45
    print('若每学期获得%d学分的优: ' % credits_for_each_sem)
    print('预计一学期后最好GPA将为%.2f(百分制%.2f)。' % (best_gpa_in_one_sem, best_gpa_in_one_sem_100))
    print('预计两学期后最好GPA将为%.2f(百分制%.2f)。' % (best_gpa_in_two_sem, best_gpa_in_two_sem_100))
    print('预计三学期后最好GPA将为%.2f(百分制%.2f)。' % (best_gpa_in_three_sem, best_gpa_in_three_sem_100))
    print('预计四学期后最好GPA将为%.2f(百分制%.2f)。' % (best_gpa_in_four_sem, best_gpa_in_four_sem_100))

    plt.show()


def main():
    file = pd.read_csv('raw_GPA.csv')
    df = pd.DataFrame(file)

    totalCredit = float(df.sum(axis=0)[0])
    print('当前总学分 =', totalCredit)
    totalPoint = df['credit'].mul(df['score']).sum(axis=0)
    GPA = round(totalPoint / totalCredit, 2)
    print('当前GPA(同济算法) = %.2f/5' % GPA)

    hundred = []
    PKUscore = []
    SJTUscore = []
    for i in df['score']:
        if i == 5:
            hundred.append(95)
            PKUscore.append(4.0)
            SJTUscore.append(4.3)
        elif i == 4:
            hundred.append(85)
            PKUscore.append(3.7)
            SJTUscore.append(3.7)
        elif i == 3:
            hundred.append(75)
            PKUscore.append(2.7)
            SJTUscore.append(3.0)
        elif i == 2:
            hundred.append(65)
            PKUscore.append(1.5)
            SJTUscore.append(2.0)
        else:
            hundred.append(30)
            PKUscore.append(0)
            SJTUscore.append(0)

    totalHundredPoint = df['credit'].mul(hundred).sum(axis=0)
    hundredPoint = round(totalHundredPoint / totalCredit, 2)
    totalPKUPoint = df['credit'].mul(PKUscore).sum(axis=0)
    PKUPoint = round(totalPKUPoint / totalCredit, 2)
    totalSJTUPoint = df['credit'].mul(SJTUscore).sum(axis=0)
    SJTUPoint = round(totalSJTUPoint / totalCredit, 2)
    print('当前百分制GPA = %.2f/100' % hundredPoint)
    print('当前GPA(北大算法) = %.2f/4' % PKUPoint)
    print('当前GPA(上海交大算法) = %.2f/4.3' % SJTUPoint)
    print()

    calGPA(GPA, totalCredit, totalPoint, totalHundredPoint)


if __name__ == '__main__':
    main()