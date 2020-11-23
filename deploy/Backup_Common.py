# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Aug.07,2020'

import os
import sys
from lib.common import logger
from lib.common import write_tar
from lib.common import write_zip
from lib.common import get_suffix
from lib.common import check_path
from lib.common import create_path
from lib.common import check_order
from lib.common import check_module
from lib.common import check_arglen
from lib.common import exit_process
from lib.common import current_time
from lib.common import break_process
from lib.common import check_package
from lib.common import get_systeminfo


def get_args():
    """
        Get arguments.
        Args: localpath, updatepath, package, module.
    """
    check_arglen(6, 6)
    local, update, backup, package, module, env = sys.argv[1:]
    logger.info('Begin to execute {} {} {} {} {} {} {}'.format(
        os.path.join(os.getcwd(), sys.argv[0]), local, update, backup, package, module, env))
    check_path(local, logger, chdir=True)
    check_package(local, package)
    check_module(local, package, module)
    create_path(backup)
    check_path(update)
    return local, update, backup, package, module, env


def backup_common():
    """
        Backup files of updatepath which will be update.
    """
    local, update, backup, package, module, env = get_args()
    backup = os.path.join(backup, 'programbak')
    create_path(backup)
    # Module's real path.
    env_path = os.path.join(local, package.split('.')[0], module, env)
    if os.path.isdir(env_path):
        target = os.path.join(backup, ''.join([env, current_time, '.zip'])) if get_systeminfo() == 'Windows' \
            else os.path.join(backup, ''.join([env, current_time, '.tar']))
        backup_list = backup_dir(env_path, update, target)
        logger.info('Backup common files successfully.')
        if backup_list:
            logger.info('Backup list:')
            for filename in backup_list:
                logger.info(filename)
        exit_process(local, package, module)
    else:
        logger.error('No such env dir {} in module'.format(env, module))
        break_process(local, package, module)


def get_namelist(path, length, file_list=[]):
    """
        Get namelist of a path.
    """
    filenames = os.listdir(path)
    for filename in filenames:
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            file_list.append(file_path[length+1:])
        else:
            get_namelist(file_path, length, file_list)
    return file_list


def backup_dir(dir_path, source, target):
    """
        Backup updatepath's files which also in the localpath's dir.
    """
    os.chdir(os.path.dirname(dir_path))
    basename = os.path.basename(dir_path)
    name_list = get_namelist(basename, len(basename))
    add_list = []
    count = 0
    package = write_zip(target) if get_systeminfo() == 'Windows' else write_tar(target)
    for name in name_list:
        source_name = os.path.join(source, name)
        if os.path.isfile(source_name):
            try:
                logger.debug('Adding file {} to package {}'.format(source_name, target))
                if get_systeminfo() == 'Windows':
                    package.write(source_name, arcname=name)
                else:
                    package.add(source_name, arcname=name)
                count += 1
            except:
                logger.error('Add file {} to package {} failed.'.format(source_name, target))
                sys.exit(1)
        else:
            add_list.append(name)
    package.close()
    name_list.clear()
    logger.info('Backup dir {} done. ENVTYPE: {}'.format(source, basename))
    logger.info('[PATH-> {} ] [file count: {} ]'.format(target, count))
    return add_list


if __name__ == "__main__":
    backup_common()