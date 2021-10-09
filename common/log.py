# -*- coding: utf-8 -*-
# Define log operation
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler


def setLog():
    logfmt = '%(asctime)s %(filename)-12s line:%(lineno)-6s [%(levelname)-6s] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logfmt,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.abspath(os.path.dirname(os.path.dirname(
                            __file__))) + os.path.sep + 'logs' + os.sep + 'auto-test_%s.log' % (time.strftime(
                            '%Y%m%d%H%M%S', time.localtime(time.time()))),
                        filemode='w',
                        )

    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(logfmt)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    Rthandler = RotatingFileHandler(
        os.path.abspath(os.path.dirname(os.path.dirname(
            __file__))) + os.path.sep + 'logs' + os.sep + 'auto-test_%s.log' % (time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))),
        maxBytes=10 * 1024 * 1024, backupCount=10)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)-12s: %(levelname)-8s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.getLogger().addHandler(Rthandler)
