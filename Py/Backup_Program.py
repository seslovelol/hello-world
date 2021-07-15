# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.02'
__date__    = 'Nov.20,2020'


import os
import sys
import configparser
from lib.common import logger
from lib.common import read_tar
from lib.common import read_zip
from lib.common import write_tar
from lib.common import write_zip
from lib.common import get_order
from lib.common import get_suffix
from lib.common import check_path
from lib.common import create_path
from lib.common import check_order
from lib.common import check_module
from lib.common import check_arglen
from lib.common import exit_process
from lib.common import current_time
from lib.common import check_package
from lib.common import get_systeminfo


def get_args():
    """
        Get arguments.
        Args: localpath, updatepath, package, module.
    """
    check_arglen(5, 5)
    local, update, backup, package, module = sys.argv[1:]
    logger.info('Begin to execute {} {} {} {} {} {}'.format(
        os.path.join(os.getcwd(), sys.argv[0]), local, update, backup, package, module))
    check_path(local, chdir=True)
    check_package(local, package)
    check_module(local, package, module)
    create_path(backup)
    check_path(update)
    order = check_order(local, package, module)
    return local, update, backup, package, module, order


def backup_program():
    """
        Backup files of updatepath which will be update.
    """
    local, update, backup, package, module, order = get_args()
    backup = os.path.join(backup, 'programbak')
    temp_path = os.path.join(local, 'log', module)
    create_path(backup)
    create_path(temp_path)
    # get content from order.txt
    content = get_order(order)
    step_all = len(content)
    step_now = 1
    add_list = []
    # Module's real path.
    module_path = os.path.join(local, package.split('.')[0], module)
    config_file = os.path.join(temp_path, 'backup_program.ini')
    remove_config(config_file)
    for name in content:
        real_path = os.path.join(module_path, name)
        package_suffix = '.zip' if get_systeminfo() == 'windows' else '.tar'
        target = os.path.join(backup, name + current_time + package_suffix)
        # script
        if name.lower().endswith(('.sh', '.py', '.bat')):
            logger.info('[ {}/{} ] {} is a script, pass.'.format(step_now, step_all, name))
            step_now += 1
        # dir
        elif os.path.isdir(real_path):
            temp = backup_dir(real_path, update, target, step_now, step_all)
            write_config(config_file, name, target)
        # package
        elif os.path.isfile(real_path) and name.lower().endswith(('.zip', '.tar')):
            temp = backup_package(real_path, update, target, step_now, step_all)
            write_config(config_file, name, target)
        # file
        elif os.path.isfile(real_path):
            temp = backup_file(name, update, target, step_now, step_all)
            write_config(config_file, name, target)
        else:
            logger.error('No such file or dir {} in {}'.format(name, local))
            sys.exit(1)
        if temp: add_list += temp
        step_now += 1
    logger.info('Program files have been backup successfully.')
    if add_list:
        write_config(config_file, 'addFileList', '|'.join(add_list), option='add program path list')
        logger.info('Not backup file list:')
        for add_file in add_list: logger.info(add_file)
    exit_process(local, package, module)


def backup_file(name, source, target, step, step_all):
    """
        Backup a file of updatepath which also in localpath.
    """
    logger.info('[ {}/{} ] {} backuping...'.format(step, step_all, name))
    source_name = os.path.join(source, name)
    add_list = []
    if os.path.isfile(source_name):
        package = write_zip(target) if get_systeminfo() == 'Windows' else write_tar(target)
        try:
            logger.debug('Adding file {} to package {}'.format(source_name, target))
            if get_systeminfo() == 'Windows':
                package.write(source_name, arcname=name)
            else:
                package.add(source_name, arcname=name)
        except:
            logger.error('Add file {} to package {} failed'.format(source_name, target))
            sys.exit(1)
        package.close()
        logger.info('Backup file {} done.'.format(name))
        logger.info('[PATH-> {} ] [file count: {} ]'.format(target, 1))
    else:
        logger.info('[ {}/{} ] {} not find in updatepath, pass'.format(step, step_all, source))
        add_list.append(source_name)
    return add_list


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


def backup_dir(dir_path, source, target, step, step_all):
    """
        Backup updatepath's files which also in the localpath's dir.
    """
    os.chdir(os.path.dirname(dir_path))
    basename = os.path.basename(dir_path)
    name_list = get_namelist(basename, len(basename))
    add_list = []
    count = 0
    logger.info('[ {}/{} ] {} backuping...'.format(step, step_all, basename))
    package = write_zip(target) if get_systeminfo() == 'Windows' else write_tar(target)
    for name in name_list:
        source_name = os.path.join(source, name)
        if os.path.exists(source_name):
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
            add_list.append(source_name)
    package.close()
    name_list.clear()
    logger.info('Backup dir {} done.'.format(basename))
    logger.info('[PATH-> {} ] [file count: {} ]'.format(target, count))
    return add_list


def backup_package(package_path, source, target, step, step_all):
    """
        Backup updatepath's files which also in the localpath's package.
    """
    add_list = []
    count = 0
    logger.info('[ {}/{} ] {} backuping...'.format(step, step_all, os.path.basename(package_path)))
    package = write_zip(target) if get_systeminfo() == 'Windows' else write_tar(target)
    suffix = get_suffix(package_path)
    local_package, name_list = read_tar(package_path) if suffix == 'tar' else read_zip(package_path)
    for name in name_list:
        source_name = os.path.join(source, name.replace(r'\/'.replace(os.sep, ''), os.sep).strip('/'))
        if os.path.exists(source_name):
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
            add_list.append(source_name)
    package.close()
    logger.info('Backup package {} done.'.format(os.path.basename(package_path)))
    logger.info('[PATH-> {} ] [file count: {} ]'.format(target, count))
    return add_list


def write_config(filepath, section, item, option='backup program path'):
    """
        Write backup files' path to a config file.
    """
    cf = configparser.ConfigParser()
    if os.path.isfile(filepath):
        cf.read(filepath)
    if section in cf.sections():
        cf.set(section, option, item)
    else:
        cf.add_section(section)
        cf.set(section, option, item)
    with open(filepath, 'w+') as f:
        cf.write(f)


def remove_config(filepath):
    """
        Clean up config files.
    """
    if os.path.isfile(filepath):
        logger.debug('Find config file {}'.format(filepath))
        try:
            os.remove(filepath)
            logger.debug('Remove config file {} successfully.'.format(filepath))
        except :
            logger.debug('Failed to remove config file {}.'.format(filepath))


if __name__ == "__main__":
    backup_program()