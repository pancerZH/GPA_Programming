

# 同济大学GPA规划工具

用于自己进行GPA规划

## 开发环境

Python3.6

- numpy 1.13.3
- pandas 0.20.3
- matplotlib 2.0.2
- beautifulsoup4 4.6.0
- requests 2.18.4

## 使用方法

### 1. 获取数据

执行

> python GPA_Programming.py

之后根据提示输入学生ID和密码即可。计算完毕后，会在当前文件夹下得到一个`goal_GPA.csv`的文件，里面记录了达到某个绩点所需要的学分，上限为200.0。

### 2. 对比分析

当获取了几份数据后可以进行绘图对比，将生成的所有csv文件存放在当前目录下，执行

> python analyse.py

即可在同一张图表中绘制所有数据源对应的折线图。