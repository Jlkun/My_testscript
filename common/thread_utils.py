# -*- coding: utf-8

import inspect
import ctypes
import logging
import threading
from mock.test_mock import TestMock
logger = logging.getLogger(__name__)

class MockServerThread(threading.Thread):
    def __init__(self, timeount=60000):
        super(MockServerThread, self).__init__()
        self.timeout = timeount

    def run(self):
        logger.info("MockServerThread 启动")
        test_mock = TestMock()
        test_mock.listen_once(timeout=self.timeout)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)