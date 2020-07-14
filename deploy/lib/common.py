# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.13,2020'


import logging
import logging.handlers
import os
from os import chdir, system
import sys
from sys import argv
import time
import tarfile
import zipfile
import ftplib
import hashlib
import shutil
import socket
import random
import platform
import subprocess


current_time = time.strftime('_%Y%m%d%H%M%S', time.localtime())
python_version = float(platform.python_version()[:3])
template_name = 'template.properties'
order_txt = 'order.txt'


def logger():
    """
        Define 2 handlers:
            handler1 is used to show messages in console.
            handler2 is used to write messages into log file.
    """
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


def check_arglen(min, max, logger):
    """
        Check argument count.
    """
    length = len(sys.argv) - 1
    if length < min:
        logger.error('')
        sys.exit(1)
    elif length > max:
        logger.error('')
        sys.exit(1)
    else:
        return length


def get_systeminfo(logger):
    """
        Get system info.
        return: Windows | Linux | Others
    """
    try:
        system_info = platform.system()
    except:
        logger.error('')
        sys.exit(1)
    else:
        return system_info


def check_file(filename, logger):
    """
        Check file.
        Exit if it does not exists.
    """
    result = True
    for _ in range(3):
        if os.path.isfile(filename):
            logger.debug('Find file {}'.format(filename))
            result = False
            break
    if result:
        logger.error('NO such file {} in current dir {}'.format(filename, os.getcwd()))
        sys.exit(1)


def change_path(path, logger):
    """
        Change path.
        Exit if it is failed.
    """
    try:
        os.chdir(path)
        logger.debug('Change to directory: {}'.format(path))
    except:
        logger.error('Change to directory: {} failed.'.format(path))
        sys.exit(1)


def check_path(path, logger, chdir=False):
    """
        Change to the path if it exists.
        Exit if it does not exist.
    """
    result = True
    for _ in range(3):
        if os.path.isdir(path):
            logger.debug('Find directory: {}'.format(path))
            if chdir:
                change_path(path, logger)
            result = False
    if result:
        logger.error('No such directory: {}'.format(path))
        sys.exit(1)


def create_path(path, logger, chdir=False):
    """
        Create a path if it does not exist.
        chdir = True: Change to the path.
    """
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
            logger.debug('Create directory: {}'.format(path))
        except:
            logger.error('Create directory: {} failed.'.format(path))
            sys.exit(1)
    if chdir:
        change_path(path, logger)


def remove_path(path, logger):
    """
        Remove path if it exists.
    """
    if os.path.isdir(path):
        logger.debug('Find directory: {}'.format(path))
        shutil.rmtree(path, ignore_errors=True)
        logger.debug('Remove directory: {} successfully.'.format(path))
    else:
        logger.debug('No such directory: {} to remove.'.format(path))


def check_ipaddr(ipaddr, logger):
    """
        Check the current device's ipaddr.
        Exit if it is not right.
    """
    local_ipaddr = socket.gethostbyname_ex(socket.gethostname())[2]
    if ipaddr in local_ipaddr:
        logger.debug('Current ip address is '.format(ipaddr))
    else:
        logger.error('Ip address error.')
        sys.exit(1)


def check_package(local, package, logger):
    """
        Check package.
        Exit if it does not exist.
    """
    package_path = os.path.join(local, package)
    if os.path.exists(package_path):
        logger.debug('Find package {} in local directory {}'.format(package, local))
    else:
        logger.error('No package {} in local directory {}'.format(package, local))
        sys.exit(1)


def check_module():


def check_order():


def get_order():


def check_template():


def read_file():


def diff_file():


def check_md5():


def get_md5():


def get_suffix():


def read_tar():


def read_zip():


def write_tar():


def write_zip():


def get_namelist():


def get_size():


def get_stat():


def extract_package():


def remove_module():


def get_ftp():


def ftp_connect():


def ftp_cwd():


def ftp_upload():


def ftp_download():


def upload_log():


def unicode_gbk():


def add_bom():


def remove_bom():


def execute_script():


def sub_process():


def break_process():


def exit_process():

