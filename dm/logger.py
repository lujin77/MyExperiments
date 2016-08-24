# -*- coding:utf-8 -*-
import logging

import logging;


def initLogger(loggerName="logger", loggerFile="E:/Code/Python/py.log", isToFile=False):
    # create a logger
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)

    # File Handler
    fileHandler = logging.FileHandler(loggerFile)
    fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'));

    # File Handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'));

    # 给logger添加handler
    if isToFile:
        logger.addHandler(fileHandler);
    logger.addHandler(consoleHandler);

    return logger;
