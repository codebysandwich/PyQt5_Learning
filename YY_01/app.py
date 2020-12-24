#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : app.py
# Author            : sanwich <122079260@qq.com>
# Date              : 2020-12-21 14:30:49
# Last Modified Date: 2020-12-24 10:33:28
# Last Modified By  : sanwich <122079260@qq.com>


import sys
import json
import pandas as pd
from script.QtDataSet import PandasModel
from script.Pollution_Draw import DrawWidget
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QDesktopWidget, QMessageBox, QMenu, QAbstractItemView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self._datapath, self._wtype = self.__load_setting()
        self.ui.setupUi(self)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setWindowTitle("天气形式数据删选")
        self.setWindowIcon(QIcon('./source/icon.png'))
        self._data = pd.DataFrame()
        self._model = PandasModel(self._data)
        self._types = []
        self.load()
        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
        self.CustomContextMenu = QMenu(self)
        # 创建选项
        self.action_draw = self.CustomContextMenu.addAction("绘图")
        self.action_reset = self.CustomContextMenu.addAction("重置")
        self.action_draw.triggered.connect(self.draw_callback)
        self.action_reset.triggered.connect(self.reset)
        # 信号槽
        self.ui.cmb_type.activated.connect(self.type_callback)
        self.ui.cmb_year.activated.connect(self.year_callback)
        self.ui.cmb_month.activated.connect(self.month_callback)
        self.ui.cmb_day.activated.connect(self.day_callback)
        self.ui.button_draw.clicked.connect(self.draw_callback)

    def load(self):
        """
        初始化tableView，初始化缓存
        """
        self._data = pd.read_excel(self._datapath, sheet_name=0, keep_default_na=False)
        self._model = PandasModel(self._data)
        self.__load_data(self._model)
        self._types = self._data[self._wtype].unique().tolist()
        # 天气形势过滤类型
        self.__reset_cmb(self.ui.cmb_type, self._types)
        self.__extra_filter()

    # ---------------私有函数--------------- #
    def __load_data(self, model):
        """
        将_model加载到tableView
        """
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(12, QHeaderView.Stretch)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(13, QHeaderView.Stretch)

    def __extra_filter(self):
        """
        将_model数据删选依据提取出来
        """
        df = self._model.toDataFrame()
        years = sorted(df.iloc[:, 0].unique().tolist())
        months = sorted(df.iloc[:, 1].unique().tolist())
        days = sorted(df.iloc[:, 2].unique().tolist())
        self.__reset_cmb(self.ui.cmb_year, years)
        self.__reset_cmb(self.ui.cmb_month, months)
        self.__reset_cmb(self.ui.cmb_day, days)

    def __reset_cmb(self, cmb, items):
        cmb.clear()
        for i, item in enumerate(items):
            cmb.insertItem(i, str(item))
        cmb.setCurrentIndex(-1)

    def __load_setting(self):
        with open('./source/setting.json', 'r') as fp:
            js = json.load(fp)
            return js['filepath'], js['type']

    # ---------------槽函数--------------- #
    def type_callback(self):
        QApplication.processEvents()
        _type = self.ui.cmb_type.currentText()
        self._model = PandasModel(self._data[self._data[self._wtype] == _type])
        QApplication.processEvents()
        self.__load_data(self._model)
        self.__extra_filter()

    def year_callback(self):
        QApplication.processEvents()
        df = self._model.toDataFrame()
        mask = df.iloc[:, 0].astype(str) == self.ui.cmb_year.currentText()
        model = PandasModel(df[mask])
        QApplication.processEvents()
        self.__load_data(model)
        self.__reset_cmb(self.ui.cmb_month, sorted(df[mask].iloc[:, 1].unique().tolist()))
        self.__reset_cmb(self.ui.cmb_day, sorted(df[mask].iloc[:, 2].unique().tolist()))

    def month_callback(self):
        QApplication.processEvents()
        df = self._model.toDataFrame()
        mask = (df.iloc[:, 1].astype(str) == self.ui.cmb_month.currentText()) & \
               (df.iloc[:, 0].astype(str) == self.ui.cmb_year.currentText())
        model = PandasModel(df[mask])
        QApplication.processEvents()
        self.__load_data(model)
        self.__reset_cmb(self.ui.cmb_day, sorted(df[mask].iloc[:, 2].unique().tolist()))

    def day_callback(self):
        QApplication.processEvents()
        df = self._model.toDataFrame()
        mask = (df.iloc[:, 1].astype(str) == self.ui.cmb_month.currentText()) & \
               (df.iloc[:, 0].astype(str) == self.ui.cmb_year.currentText()) & \
               (df.iloc[:, 2].astype(str) == self.ui.cmb_day.currentText())
        model = PandasModel(df[mask])
        QApplication.processEvents()
        self.__load_data(model)

    def draw_callback(self):
        if not self.ui.tableView.selectedIndexes():
            QMessageBox.warning(self, "提示", "请选择需要绘图的数据！")
            return
        index = self.ui.tableView.currentIndex().row()
        ser = self.ui.tableView.model().toDataFrame().iloc[index, 0:3]
        year, month, day = ser['年'], ser['月'], ser['日']
        draw = DrawWidget(self._datapath, year, month, day)
        draw.show()

    def reset(self):
        QApplication.processEvents()
        self._model = PandasModel(self._data)
        QApplication.processEvents()
        self.__load_data(self._model)
        self.ui.cmb_type.setCurrentIndex(-1)
        self.__extra_filter()

    def show_menu(self):
        if self.ui.tableView.geometry().contains(QCursor.pos()):
            self.CustomContextMenu.exec_(QCursor.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
