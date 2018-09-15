# -*- coding:utf-8 -*-
import pandas as pd
import os, sys
import matplotlib.pyplot as plt

def main():
    dfs = []
    filename = []
    path = sys.path[0]
    dirs = os.listdir(path)
    for i in dirs:
        if os.path.splitext(i)[1] == ".csv":   # 筛选csv文件
            dfs.append(pd.read_csv(i))
            filename.append(os.path.splitext(i)[0])
            print('{} loaded'.format(i))
    
    lines = []
    for df in dfs:
        line, = plt.plot(df['"A" credits needed'], df['Goal GPA'])
        lines.append(line)
    plt.legend(lines, filename, loc='lower right')
    plt.show()


if __name__ == "__main__":
    main()