# -*- coding: utf-8 -*-
import logging.handlers


class LogUtils(object):

    @staticmethod
    def createLogger(loggerName,loggerPath):  # 日志
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        datefmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        # 数据日志输出
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)
        # create file handler
        fh = logging.handlers.RotatingFileHandler(filename=loggerPath,encoding="utf8")
        fh.setLevel(logging.INFO)
        # create formatter
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger