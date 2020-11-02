# -*- encoding: utf-8 -*-
'''
@Author: sandwich
@Date: 2020-10-30 14:53:57
@LastEditTime: 2020-10-30 14:53:59
@LastEditors: sandwich
@Description: 可以挂起与启动的线程
@FilePath: /PyQt5_Learning/script/timer.py
'''

import threading
from time import time, sleep

class Thread_(threading.Thread):
    def __init__(self, period, target, args=()) -> None:
        super(Thread_, self).__init__()
        self.__running = threading.Event()
        self.__running.set()
        self.__period = period
        self.__target = target
        self.__args = args

    def run(self) -> None:
        while self.__running.is_set():
            self.__target(*self.__args)
            sleep(self.__period)


    def stop(self):
        self.__running.clear()

class Timer():
    def __init__(self, target, args=()) -> None:
        self.__target = target
        self.__args = args

    def setInterval(self, msc: int):
        self.__interval = msc / 1000

    def start(self):
        self._thread = Thread_(self.__interval, self.__target, self.__args)
        self._thread.setDaemon(True)
        self._thread.start()
        # self._thread.join()

    def stop(self):
        if self._thread:
            self._thread.stop()


if __name__ == "__main__":
    def test(name):
        print(time())
        print(name)
    timer = Timer(target=test, args=('hello', ))
    timer.setInterval(1000)
    timer.start()
    sleep(3)
    timer.stop()
    sleep(3)
    timer.start()
    sleep(3)
    timer.stop()