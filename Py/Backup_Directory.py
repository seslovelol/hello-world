# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.30,2020'


import os
import sys
from lib.common import logger
from lib.common import write_tar
from lib.common import write_zip
from lib.common import check_path
from lib.common import create_path
from lib.common import current_time
from lib.common import check_arglen
from lib.common import get_systeminfo


def get_args():
    """
        Get args.
        Args: targetpath, sourcepath, excludepath.
    """
    exclude = ''
    arg_len = check_arglen(2, 3)
    target, source = sys.argv[1:3]
    if arg_len == 3:
        exclude = sys.argv[3]
    logger.info('Begin to execute {} {} {} {} FTPINFO'.format(
        os.path.join(os.getcwd(), sys.argv[0]), target, source, exclude
    ))
    create_path(target)
    check_path(source)
    exclude = check_exclude(exclude, source)
    return source, target, exclude


def check_exclude(exclude_path, source_path):
    """
        Remove elements from source list if they do not exist.
    """
    exclude_list = exclude_path.split(',')
    [exclude_list.remove(f) for f in list(exclude_list) if not os.path.exists(os.path.join(source_path, f))]
    return exclude_list


def backup_path():
    """
        Backup a path to a package.
            Package type is zip if system is Windows.
            Package type is tar if system is Linux.
    """
    source, target, exclude = get_args()
    start_path = os.path.dirname(source)
    base_name = os.path.basename(source.rstrip('/').rstrip('\\'))
    target = os.path.join(target, 'backup')
    create_path(target)
    platform = get_systeminfo()
    package_name = os.path.join(target, ''.join([base_name, '.bak', current_time, '.zip'])) if platform == 'Windows' \
        else os.path.join(target, ''.join([base_name, '.bak', current_time, '.tar']))
    package_file = write_zip(package_name) if platform == 'Windows' \
        else write_tar(package_name)
    # Get a 3-tuple of source path.
    for root, dirs, files in os.walk(source):
        # Remove exclude files or dirs from source path.
        [dirs.remove(d) for d in list(dirs) if d in exclude]
        [files.remove(f) for f in list(files) if f in exclude]
        relroot = os.path.relpath(root, start=start_path)
        # Add files of source path to package.
        for file_name in files:
            try:
                if platform == 'Windows':
                    package_file.write(os.path.join(root, file_name), arcname=os.path.join(relroot, file_name))
                else:
                    package_file.add(os.path.join(root, file_name), arcname=os.path.join(relroot, file_name))
                logger.debug('Adding file {} to package.'.format(os.path.join(root, file_name)))
            except:
                logger.error('Failed to add file {} to package.'.format(os.path.join(root, file_name)))
                sys.exit(1)
        # Add dirs of source path to package.
        for dir_name in dirs:
            try:
                if platform == 'Windows':
                    package_file.write(os.path.join(root, dir_name), arcname=os.path.join(relroot, dir_name))
                else:
                    package_file.add(os.path.join(root, dir_name), arcname=os.path.join(relroot, dir_name))
                logger.debug('Adding file {} to package.'.format(os.path.join(root, dir_name)))
            except:
                logger.error('Failed to add file {} to package.'.format(os.path.join(root, dir_name)))
                sys.exit(1)
    package_file.close()
    logger.info('Backup {} successfully.'.format(base_name))
    logger.info('Backup from {} to {}'.format(source, package_name))
    print(0)
    sys.exit(0)


if __name__ == "__main__":
    backup_path()