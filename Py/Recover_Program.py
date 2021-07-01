# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.0'
__date__    = 'Nov.20,2020'

import os
import sys
import time
import stat
import logging
import configparser
import logging.handlers
from lib.common import logger
from lib.common import read_zip
from lib.common import read_tar
from lib.common import get_stat
from lib.common import check_path
from lib.common import get_suffix
from lib.common import create_path
from lib.common import file_logger
from lib.common import check_arglen


def get_args():
    """
        Get args: localpath, updatepath, backuppath, module.
    """
    check_arglen(4, 4)
    local, update, backup, module = sys.argv[1:]
    logger.info('Begin to execute {} {} {} {} {}'.format(
        os.path.join(os.getcwd(), sys.argv[0]), local, update, backup, module))
    check_path(local)
    check_path(update)
    check_path(backup)
    return local, update, backup, module


def recover_program():
    """
        Recover files from backuppath to updatepath.
    """
    local, update, backup, module = get_args()
    temp_path = '/'.join((local, 'log', module))
    create_path(temp_path)
    handler, temp_log = file_logger(temp_path, 'recover_program')
    config_file = os.path.join(temp_path, 'backup_program.ini')
    sections = read_config(config_file)
    # Get content from config.
    content = sections.keys()
    # Define all steps and step now.
    step_all = len(content)
    step_now = 1
    for name in content:
        if name == 'addFileList':
            logger.info('[ {}/{} ] {} removing...'.format(step_now, step_all, name))
            for filename in sections[name]['add program path list'].split('|'):
                try:
                    os.remove(filename)
                    logger.debug('{} has been removed.'.format(filename))
                except FileNotFoundError:
                    logger.debug('{} has been removed yet.'.format(filename))
            logger.info('All added files have been removed')
        else:
            real_path = sections[name]['backup program path']
            if os.path.isfile(real_path):
                result = copy_package(real_path, update, step_all, step_now)
                get_stat(result)
        step_now += 1
    logger.removeHandler(handler)
    sys.exit(0)


def copy_package(source, target, step_all, step):
    """
        Extract files and dirs from package, then copy them to target dir.
    """
    suffix = get_suffix(source)
    base_name = os.path.basename(source)
    package_file, name_list = read_tar(source) if suffix == 'tar' else read_zip(source)
    logger.info('[ {}/{} ] {} recovering...'.format(step, step_all, base_name))
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


def read_config(filepath):
    """
        Read sections from a config file.
    """
    if os.path.isfile(filepath):
        cf = configparser.ConfigParser()
        cf.read(filepath)
        sections = cf._sections
    else:
        logger.debug('No config file: {}'.format(filepath))
        sections = ""
    return sections


if __name__ == "__main__":
    recover_program()