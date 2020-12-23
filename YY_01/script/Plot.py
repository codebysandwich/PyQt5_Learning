#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : Plot.py
# Author            : sanwich <122079260@qq.com>
# Date              : 2020-12-23 15:54:09
# Last Modified Date: 2020-12-23 15:54:09
# Last Modified By  : sanwich <122079260@qq.com>

import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def draw(df, ax):
    ax.plot([1, 3, 4])

if __name__ == "__main__":
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    draw(None, ax)
    plt.show()
