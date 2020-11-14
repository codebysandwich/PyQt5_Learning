# PyQt5_Learning
pyqt5学习仓库

## PyQt结合matplot绘图
+ 创建mpl-FigureCanvas控件，布局到QWidget中
    + 点击按钮可以刷新控件绘图
    + 控件接受数据实现动态绘图
        1. 使用QTimer实现
        2. 使用重载线程方式实现（script/timer.py）
