# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import login_xuanke as xk
import requests


def calGPA(GPA, totalCredit, totalPoint, totalHundredPoint):
    """ 计算需要争取的优秀学分计算函数为
    (totalCredit * goal - totalPoint) / (5 - goal) """
    goalGPA = []
    result = []
    hundredResult = []
    boundary = 4.95
    for i in np.arange(GPA+0.01, boundary, 0.01):
        x = (totalCredit * i - totalPoint) / (5 - i)
        goalGPA.append(round(i, 2))
        result.append(round(x, 1))
        hundredPoint = round(((totalHundredPoint + x * 95) / (totalCredit + x)), 1)
        hundredResult.append(hundredPoint)

    rawData = {'Goal GPA': goalGPA, '"A" credits needed': result, 'GPA in 100': hundredResult}
    dfResult = pd.DataFrame(rawData, columns=['Goal GPA', '"A" credits needed', 'GPA in 100'])
    dfResult.to_csv('goal_GPA.csv')

    plt.plot(goalGPA, result)
    # print('{}:\t{}\t{}'.format('目标GPA', '需要的优秀学分', '百分制'))
    # for i in zip(goalGPA, result, hundredResult):
        # print('{}:\t{}\t{}'.format(i[0], i[1], i[2]))
    best_gpa_in_one_year = (totalPoint + 20 * 2 * 5) / (totalCredit + 40)
    best_gpa_in_100 = (totalPoint + 20 * 2 * 5) / (totalCredit + 40) * 10 + 45
    print('若每学期获得20学分的优，预计一年后最好绩点是%.2f(百分制%.2f)。' % (best_gpa_in_one_year, best_gpa_in_100))

    plt.show()


def main():
    s = requests.session()
    header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    credits = []
    points = []
    username = input('Please enter your student ID: ')
    password = input('Please enter your password:   ')
    xk.login(header, s, username, password)
    xk.get_score(header, s, credits, points)
    data = {
        'credits': credits,
        'points': points
    }
    df = pd.DataFrame(data)

    totalCredit = float(df.sum(axis=0)[0])
    print('当前总学分 =', totalCredit)
    totalPoint = df['credits'].mul(df['points']).sum(axis=0)
    GPA = round(totalPoint / totalCredit, 2)
    print('当前总绩点 =', GPA)

    hundred = []
    for i in df['points']:
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
    totalHundredPoint = df['credits'].mul(hundred).sum(axis=0)
    hundredPoint = round(totalHundredPoint / totalCredit, 1)
    print('当前百分制学分 =', hundredPoint)

    calGPA(GPA, totalCredit, totalPoint, totalHundredPoint)


if __name__ == '__main__':
    main()