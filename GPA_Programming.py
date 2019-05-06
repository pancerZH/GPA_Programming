# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import login_xuanke as xk
import requests
import getpass


def calGPA(GPA, totalCredit, totalPoint, totalHundredPoint):
    """ 计算需要争取的优秀学分计算函数为
    (totalCredit * goal - totalPoint) / (5 - goal) """
    goalGPA = []
    result = []
    hundredResult = []

    for i in np.arange(0.5, 200.0, 0.5):
        new_gpa = round((totalPoint + i * 5) / (totalCredit + i), 2)
        if new_gpa not in goalGPA:
            goalGPA.append(new_gpa)
            result.append(i)
            hundredPoint = round(((totalHundredPoint + i * 95) / (totalCredit + i)), 2)
            hundredResult.append(hundredPoint)


    rawData = {'Goal GPA': goalGPA, '"A" credits needed': result, 'GPA in 100': hundredResult}
    dfResult = pd.DataFrame(rawData, columns=['Goal GPA', '"A" credits needed', 'GPA in 100'])
    dfResult.to_csv('goal_GPA.csv')

    plt.plot(result, goalGPA)
    best_gpa_in_one_year = (totalPoint + 20 * 2 * 5) / (totalCredit + 40)
    best_gpa_in_100 = (totalPoint + 20 * 2 * 5) / (totalCredit + 40) * 10 + 45
    print(u'若每学期获得20学分的优，预计一年后最好绩点是%.2f(百分制%.2f)。' % (best_gpa_in_one_year, best_gpa_in_100))

    plt.show()


def calRealGPA(GPA, totalCredit, totalPoint, totalHundredPoint):
    print(GPA)
    print(totalCredit)
    print(totalPoint)
    print(totalHundredPoint)

    A = float(input('Please enter your A credits: '))
    B = float(input('Please enter your B credits: '))
    totalCredit = totalCredit + A + B
    totalPoint = totalPoint + A * 5 + B * 4
    GPA = totalPoint / (totalCredit * 5) * 5
    totalHundredPoint = GPA * 10 + 45

    print(GPA)
    print(totalCredit)
    print(totalPoint)
    print(totalHundredPoint)


def main():
    s = requests.session()
    header={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    credits = []
    points = []
    username = input('Please enter your student ID: ')
    password = getpass.getpass('Please enter your password: ')
    xk.login(header, s, username, password)
    xk.get_score(header, s, credits, points)
    data = {
        'credits': credits,
        'points': points
    }
    df = pd.DataFrame(data)

    totalCredit = float(df.sum(axis=0)[0])
    print(u'当前总学分 =', totalCredit)
    totalPoint = df['credits'].mul(df['points']).sum(axis=0)
    GPA = round(totalPoint / totalCredit, 2)
    print(u'当前总绩点 =', GPA)

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
    print(u'当前百分制学分 =', hundredPoint)

    #calGPA(GPA, totalCredit, totalPoint, totalHundredPoint)
    calRealGPA(GPA, totalCredit, totalPoint, totalHundredPoint)


if __name__ == '__main__':
    main()