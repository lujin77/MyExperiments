# -*- coding:utf-8 -*-

"""

日志初始化函数

"""

import sys
import time

import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler


def init_logger(logger_name):
	if logger_name not in Logger.manager.loggerDict:
		logger = logging.getLogger(logger_name)
		logger.setLevel(logging.DEBUG)
		# handler all
		handler = TimedRotatingFileHandler('./all.log', when='midnight', backupCount=7)
		datefmt = "%Y-%m-%d %H:%M:%S"
		format_str = "[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s"
		formatter = logging.Formatter(format_str, datefmt)
		handler.setFormatter(formatter)
		handler.setLevel(logging.INFO)
		logger.addHandler(handler)
		# handler error
		handler = TimedRotatingFileHandler('./error.log', when='midnight', backupCount=7)
		datefmt = "%Y-%m-%d %H:%M:%S"
		format_str = "[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s"
		formatter = logging.Formatter(format_str, datefmt)
		handler.setFormatter(formatter)
		handler.setLevel(logging.ERROR)
		logger.addHandler(handler)

	logger = logging.getLogger(logger_name)
	return logger


logger = init_logger('dataservice')

if __name__ == '__main__':
	logger = init_logger('dataservice')
	logger.error("test-error")
	logger.info("test-info")
	logger.warn("test-warn")
