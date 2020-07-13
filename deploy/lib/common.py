# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.13,2020'


from logging import Handler
import os
import sys
import time
import tarfile
import zipfile
import ftplib
import hashlib
import shutil
import random
import platform
import subprocess
import logging
import logging.handlers


current_time = time.strftime('_%Y%m%d%H%M%S', time.localtime())
template_name = 'template.properties'
order_txt = 'order.txt'
python_version = float(platform.python_version()[:3])


def logger():
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    handler1 = logging.StreamHandler()
    handler1.setLevel(logging.INFO)
    handler1.setFormatter(logging.Formatter("%(asctime)s" - "%(message)s"))
    logger.addFilter(handler1)
    log_path = os.path.join(os.getcwd(), 'log')
    if not os.path.isdir(log_path):
        try:
            os.makedirs(log_path)
            print('Log path: {}'.format(log_path))
        except:
            print('Warning: Create log directory failed.')
    handler2 = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, 'run.log'), when='W0', interval=1, backupCount=0)
    handler2.setFormatter("%(asctime)s" - "%(levelname)s" - "%(message)s"))
    logger.addHandler(handler2)
    return logger