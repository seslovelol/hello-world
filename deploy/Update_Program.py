# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.30,2020'


import os
import sys
import time
import shutil
import locale
import logging
from lib.common import logger
from lib.common import add_bom
from lib.common import get_stat
from lib.common import read_tar
from lib.common import read_zip
from lib.common import get_order
from lib.common import check_ftp
from lib.common import get_suffix
from lib.common import upload_log
from lib.common import check_path
from lib.common import create_path
from lib.common import check_order
from lib.common import check_module
from lib.common import check_arglen
from lib.common import exit_process
from lib.common import check_package
from lib.common import python_version
from lib.common import execute_script


def get_args(logger):
    """
        Get args.
        Args: localpath, updatepath, packagename, module, ftpinfo
    """
    check_arglen(5, 5, logger)
    local, update, package, module, ftpinfo = sys.argv[1:]
    logger.info('Begin to execute {} {} {} {} {} FTPINFO'.format(
        os.path.join(os.getcwd(), sys.argv[0]), local, update, package, module
    ))
    check_path(local, logger)
    check_package(local, package, logger)
    check_module(local, package, module, logger)
    create_path(update, logger)
    ftpinfo = check_ftp(ftpinfo, logger)
    order = check_order(local, package, module, logger)
    return local, update, package, module, ftpinfo, order


def update_program(logger):
    """
        Update files from localpath to updatepath.
    """
    logger = logger()
    local, update, package, module, ftpinfo, order = get_args(logger)
    temp_path = '/'.join((local, 'log', module))
    create_path(temp_path, logger)
    handler, temp_log = file_logger(temp_path, logger)
    # Get content list from order.txt
    content = get_order(order, logger)
    step_all = len(content)
    step_now = 1
    # Module's real path.
    module_path = os.path.join(local, package.split('.')[0], module)
    for name in content:
        real_path = os.path.join(module_path, name)
        # scripts
        if name.endswith(('.py', '.bat', '.sh')):
            logger.info('[ {}/{} ] {} executing...'.format(step_now, step_all, name))
            execute_script(real_path, logger)
            step_now += 1
        # dirs
        elif os.path.isdir(real_path):
            logger.info('[ {}/{} ] {} updating...'.format(step_now, step_all, name))
            result = copy_dir(real_path, update, logger)
            logger.info('Copy tree {} to {} successfully.'.format(name, update))
            get_stat(result, logger)
            step_now += 1
        # packages
        elif os.path.isfile(real_path) and name.endswith(('.zip', '.tar')):
            result = copy_package(real_path, update, local, step_all, step_now, logger)
            get_stat(result, logger)
            step_now += 1
        # files
        elif os.path.isfile(real_path):
            result = copy_file(real_path, update, step_all, step_now, logger)
            get_stat(result, logger)
            step_now += 1
        # error
        else:
            logger.error('File or dir {} can not find in module {}'.format(name, module_path))
            sys.exit(0)
    logger.removeHandler(handler)
    add_bom(temp_log)
    upload_log(package, module, ftpinfo, temp_log, logger)
    exit_process(local, package, module, logger)


def file_logger(path, logger):
    """
        Write messages to a log file.
    """
    log_name = time.strftime('%Y%m%d%H%M%S_update.log', time.localtime())
    log_path = os.path.join(path, log_name)
    handler = logging.FileHandler(log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return handler, log_path


def copy_file(source, target, step_all, step, logger):
    """
        Copy a file to target path.
    """
    base_name = os.path.basename(source)
    target_name = os.path.join(target, base_name)
    file_list = []
    if os.path.isfile(target_name):
        file_list.append(target_name)
    logger.info('[ {}/{} ] {} updating...'.format(step, step_all, base_name))
    try:
        shutil.copy(source, target_name)
    except:
        logger.error('Failed to copy file {}'.format(base_name))
        sys.exit(1)
    logger.info('Copy file {} to {} successfully.'.format(base_name, target))
    return file_list


def copy_dir(source, target, logger, copy_list=[]):
    """
        Copy sub files and dirs from source path to target path.
    """
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        target_path = os.path.join(target, name)
        if os.path.isfile(source_path):
            if os.path.isfile(target_path):
                copy_list.append(target_path)
            shutil.copy(source_path, target_path)
        else:
            if not os.path.isdir(target_path):
                logger.debug('Create target dir {} copy.'.format(target_path))
                os.makedirs(target_path)
            copy_dir(source_path, target_path, logger)
    return copy_list


def copy_package(source, target, local, step_all, step, logger):
    """
        Extract files to target path.
    """
    suffix = get_suffix(source, logger)
    base_name = os.path.basename(source)
    package_file, name_list = read_tar(source, logger) if suffix == 'tar' else read_zip(source, logger)
    logger.info('[ {}/{} ] {} updating...'.format(step, step_all, base_name))
    cover_list = []
    for name in name_list:
        # file_name = os.path.join(target, name) if suffix == 'tar' else os.path.join(target, name.encode('cp437').decode(locale.getpreferredencoding()))
        file_name = os.path.join(target, name)
        if os.path.isfile(file_name):
            cover_list.append(file_name)
    if suffix == 'tar' or suffix == 'zip' and python_version[1] > 5:
        try:
            package_file.extractall(target)
        except:
            logger.error('Extract {} from package {} failed.'.format(base_name, target))
            package_file.close()
            sys.exit(1)
    if suffix == 'zip' and python_version[1] < 6:
        try:
            for name in name_list:
                new_name = name.encode('cp437').decode(locale.getpreferredencoding())
                logger.debug('Extracting: {}'.format(new_name))
                package_file.extract(name, new_name)
            package_file.close()
            logger.debug('Extract {} done.'.format(base_name))
        except:
            logger.error('Failed to extract package {}'.format(base_name))
            package_file.close()
            sys.exit(1)
    package_file.close()
    logger.info('Extract package {} to {} successfully.'.format(base_name, target))
    return cover_list


if __name__ == "__main__":
    update_program(logger)