# -*- coding: utf-8
import configparser,os

confFieName = 'conf.ini'

def getconfig():
    config = configparser.RawConfigParser()
    config.read(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + os.path.sep + 'common' + os.path.sep + confFieName,encoding='utf8')
    return config

def getCert(name):
    """
    :param name:
    :return:
    """
    return os.path.dirname(
        os.path.dirname(__file__)) + os.path.sep + "cert\\" + name

