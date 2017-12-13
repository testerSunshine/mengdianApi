# coding: utf-8

import os
import time
import logging

logger = None
loggerHandler = None
dateStr = ''  # 默认拥有日期后缀
suffix = ''  # 除了日期外的后缀


def setSuffix(s):
    global suffix
    suffix = s


def getTodayDateStr():
    return time.strftime("%Y-%m-%d", time.localtime(getNowTimestamp()))


def setDateStr(s):
    global dateStr
    dateStr = s


def isAnotherDay(s):
    global dateStr
    return dateStr != s


def getLogFile():
    global dateStr, suffix
    rtn = os.path.join(getLogDir(), dateStr)
    if suffix:
        rtn += "_" + suffix
    return rtn + ".log"


def log(msg, func="info"):
    global logger
    if not logger:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    todayStr = getTodayDateStr()
    if isAnotherDay(todayStr):
        setDateStr(todayStr)
        logger.removeHandler(loggerHandler)

        fh = logging.FileHandler(getLogFile())
        fm = logging.Formatter(u'[%(asctime)s][%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)')
        fh.setFormatter(fm)

        logger.addHandler(fh)

    levels = {
        "debug": logger.debug,
        "info": logger.info,
        "warning": logger.warning,
        "error": logger.error,
        "critical": logger.critical
    }

    levels[func](msg)


def getNowTimestamp():
    return time.time()


def decMakeDir(func):
    def handleFunc(*args, **kwargs):
        dirname = func(*args, **kwargs)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif not os.path.isdir(dirname):
            pass
        return dirname
    return handleFunc


def getWorkDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@decMakeDir
def getTmpDir():
    return os.path.join(getWorkDir(), "tmp")


@decMakeDir
def getLogDir():
    return os.path.join(getTmpDir(), "log")

