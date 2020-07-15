# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.13,2020'


import logging
import logging.handlers
import os
import sys
from sys import modules
import time
import locale
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
    handler2.setFormatter("%(asctime)s" - "%(levelname)s" - "%(message)s")
    logger.addHandler(handler2)
    return logger


def check_arglen(min, max, logger):
    """
        Check argument count.
    """
    length = len(sys.argv) - 1
    if length < min:
        logger.error('too few arguments.')
        sys.exit(1)
    elif length > max:
        logger.error('too much arguments.')
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
        logger.error('Can not get system info.')
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
        logger.debug('Change to directory: {} successfully.'.format(path))
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


def get_suffix(file_name, logger, package=True):
    """
        Get suffix of a filename.
        Args: tar | zip | other
    """
    file_suffix = file_name.split('.')[-1]
    if package:
        if file_suffix in ('tar', 'zip'):
            return file_suffix
        else:
            logger.error('{} is not a package.'.format(file_name))
            sys.exit(1)
    else:
        return file_suffix


def read_tar(package_name, logger):
    """
        Open a tarfile for reading.
    """
    if tarfile.is_tarfile(package_name):
        try:
            tar_file = tarfile.open(package_name, 'r')
            name_list = tar_file.getnames()
            return tar_file, name_list
        except:
            logger.error('Read package {} failed.'.format(package_name))
            sys.exit(1)
    else:
        logger.error('{} is not a tar file.'.format(package_name))
        sys.exit(1)


def read_zip(package_name, logger):
    """
        Open a zipfile for reading.
    """
    if zipfile.is_zipfile(package_name):
        try:
            zip_file = zipfile.ZipFile(package_name, 'r')
            name_list = zip_file.namelist()
            return zip_file, name_list
        except:
            logger.error('Read package {} failed.'.format(package_name))
            sys.exit(1)
    else:
        logger.error('{} is not a zip file.'.format(package_name))
        sys.exit(1)


def write_tar(package_name, logger):
    """
        Open a tar file for writing.
    """
    try:
        tar_file = tarfile.open(package_name, 'w')
        return tar_file
    except:
        logger.error('Write package {} failed.'.format(package_name))
        sys.exit(1)


def write_zip(package_name, logger):
    """
        Open a zip file for writing.
    """
    try:
        zip_file = zipfile.ZipFile(package_name, 'w')
        return zip_file
    except:
        logger.error('Write package {} failed.'.format(package_name))
        sys.exit(1)


def get_namelist(local, package_name, logger):
    """
        Get package's namelist.
    """
    suffix = get_suffix(package_name, logger)
    package_path = os.path.join(local, package_name)
    package, name_list = read_tar(package_path, logger) if suffix == 'tar' else read_zip(package_path, logger)
    package.close()
    return name_list


def get_size(size, is_disk=True):
    """
        Get size of a file.
    """
    formats = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    unit = 1024.0 if is_disk else 1000.0
    if not (isinstance(size, float) or isinstance(size, int)):
        raise TypeError('Not a number.')
    if size < 0:
        raise ValueError('Less than 0.')
    for i in formats:
        if size < unit:
            return '{0:.1f} {1}'.format(size, i)
        else:
            size /= unit


def get_stat(file_list, logger):
    """
        Get stat of a file.
    """
    if file_list:
        for file_name in file_list:
            file_info = os.stat(file_name)
            file_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info.st_atime))
            file_size = get_size(file_info.st_size)
            logger.info('{}    {}    {}'.format(file_name, file_time, file_size))
        file_list.clear()


def check_md5(file_name, logger):
    """
        Check file's md5.
    """
    local_md5 = get_md5(file_name)
    md5_file = '.'.join([file_name, 'md5'])
    remote_md5 = read_file(md5_file, logger, exclude=True)[0]
    logger.info("Local file {}'s MD5 code: {}".format(file_name, local_md5))
    logger.info("Remote file {}'s value: {}".format(md5_file, remote_md5))
    if local_md5 == remote_md5:
        logger.info('')
        logger.info('MD5 codes are equal , data integrity.')
    else:
        logger.error('MD5 codes are different, data loss.')
        sys.exit(1)


def get_md5(file_name):
    """
        Get md5 of a file.
    """
    m = hashlib.md5()
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def read_file(filename, logger, exclude=False):
    """
        Read a file and return the file's content.
    """
    if os.path.isfile(filename):
        try:
            file_reader = open(filename, 'r')
            content = file_reader.read().splitlines()
        except:
            file_reader = open(filename, 'r', encoding='utf-8-sig')
            content = file_reader.read().splitlines()
        finally:
            if exclude:
                # Remove the lines with '#' or the empty lines from content.
                [content.remove(t) for t in list(content) if t.startwith('#') or t == '']
                new_content = []
                for c in content:
                    new_content.append(c.strip())
                content = new_content
            file_reader.close()
    else:
        logger.error('No such file: {}'.format(filename))
        sys.exit(1)


def extract_package(local, package_name, module, logger):
    """
        Extract files from package.
    """
    suffix = get_suffix(package_name, logger)
    package_path = os.path.join(local, package_name)
    package, name_list = read_tar(package_path, logger) if suffix == 'tar' else read_zip(package_path, logger)
    change_path(local, logger)
    remove_path(os.path.join(local, module), logger)
    if suffix == 'tar':
        try:
            for name in name_list:
                if module in name:
                    logger.debug('Extracting: {}'.format(name))
                    package.extract(name)
            package.close()
            logger.debug('Extract {} done'.format(module))
        except:
            logger.error('Extract {} from package {} failed.'.format(module, package_name))
            package.close()
            sys.exit(1)
    else:
        try:
            for name in name_list:
                new_name = name.encode('cp437').decode(locale.getpreferredencoding())
                if module in new_name:
                    logger.debug('Extracting: {}'.format(new_name))
                    package.extract(name, new_name)
            package.close()
            logger.debug('Extract {} done.'.format(module))
        except:
            logger.error('Extract {} from package {} failed.'.format(module, package_name))
            package.close()
            sys.exit(1)


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


def check_module(local, package, module, logger, extract=True):
    """
        Check module from package.
        Exit if it does not exist.
    """
    name_list = get_namelist(local, package, logger)
    temp = '/'.join([package.split('.')[0], module])
    module_path = temp if get_suffix(package, logger) else temp + '/'
    if module_path in name_list:
        logger.debug('Find module {} in package {}'.format(module, package))
    else:
        logger.error('No module {} in package {}. Check your package.'.format(module, package))
    if extract:
        extract_package(local, package, module_path, logger)


def remove_module(local, package, module, logger):
    """
        Clean up the module directory.
    """
    path = '/'.join([package.split('.')[0], module])
    change_path(local, logger)
    remove_path(path, logger)


def check_order(local, package, module, logger, extract=True):
    """
        Check order.txt from package/module.
        Extract it from package if it exists.
    """
    name_list = get_namelist(local, package, logger)
    order_path = '/'.join([package.split('.')[0], module, order_txt])
    if order_path in name_list:
        logger.debug('Find order.txt in package.')
    else:
        logger.error('No order.txt in package. Check your package.')
        sys.exit(1)
    if extract:
        extract_package(local, package, order_path, logger)
    return os.path.join(local, order_path)


def get_order(order, logger):
    """
        Get content of `order.txt`.
    """
    content = read_file(order, logger, exclude=True)
    return content


def check_template(local, package, logger, extract=True):
    """
        Check template from package.
        Extract it from package if it exists.
    """
    name_list = get_namelist(local, package, logger)
    template_path = '/'.join([package.split('.')[0], template_name])
    if template_path in name_list:
        logger.info('Find template file in package.')
    else:
        logger.error('No template file in package. Check your package.')
        sys.exit(1)
    if extract:
        extract_package(local, package, template_path, logger)
    return os.path.join(local, template_path)


def diff_file():


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


def break_process(local, package, module, logger, clean_up=True):
    """
        Clean up module directory and break process.
        Just exit process and do not remove module directory if clean_up is False.
        Set clean_up `False` if it is a database update.
    """
    if clean_up:
        remove_module(local, package, module, logger)
    print(1)
    sys.exit(1)


def exit_process(local, package, module, logger, clean_up=True):
    """
        Clean up module directory and exit process.
        Just exit process and do not remove module directory if clean_up is False.
        Set clean_up `False` if it is a database update.
    """
    if clean_up:
        remove_module(local, package, module, logger)
    print(0)
    sys.exit(0)