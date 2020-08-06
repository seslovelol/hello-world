# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.29,2020'


import os
import sys
import shutil
from lib.common import logger
from lib.common import ftp_cwd
from lib.common import get_ftp
from lib.common import check_ftp
from lib.common import check_md5
from lib.common import create_path
from lib.common import current_time
from lib.common import check_arglen
from lib.common import ftp_download


def get_args(logger):
    """
        Get args.
        Args: packagename, localpath, short, code, ftpinfo.
    """
    check_arglen(5, 5, logger)
    package, local, short, code, ftpinfo = sys.argv[1:]
    logger.info('Begin to execute {} {} {} {} FTPINFO'.format(
        os.path.join(os.getcwd(), sys.argv[0]), package, local, short, code
    ))
    ftpinfo = check_ftp(ftpinfo, logger)
    return package, local, short, code, ftpinfo


def download_package(logger):
    """
        Download a package and a file which record it's md5 code.
    """
    logger = logger()
    package, local, short, code, ftpinfo = get_args(logger)
    remote = os.path.join(ftpinfo[4], short, code).replace('\\', '/') + '/'
    local = os.path.join(local, code)
    logger.info('localPath = {}'.format(local))
    logger.info('remotePath = {}'.format(remote))
    logger.info('remoteFile = {}'.format(package))
    package_md5 = '.'.join([package, 'md5'])
    check_path(local, logger)
    package_result = False
    md5_result = False
    client = get_ftp(ftpinfo, logger, message=True)
    remove_package(package, logger)
    remove_package(package_md5, logger)
    ftp_cwd(client, remote, logger)
    package_result = ftp_download(client, package, logger)
    md5_result = ftp_download(client, package_md5, logger)
    client.quit()
    if package_result and md5_result:
        check_md5(package, logger)
        sys.exit(0)
    else:
        logger.error('Failed to download package.')
        sys.exit(1)


def remove_package(package, logger):
    """
        Clean up history packages.
    """
    if os.path.isfile(package):
        try:
            os.remove(package)
            logger.debug('Remove history package {} successfully.'.format(package))
        except:
            logger.debug('Failed to remove history package {}'.format(package))


def check_path(path, logger):
    """
        Backup history packages.
    """
    try:
        dir_list = os.listdir(path)
        if dir_list:
            dest = os.path.join(os.path.dirname(path), os.path.basename(path) + current_time)
            logger.info('Backup localpath: {}'.format(path))
            shutil.move(path, dest)
        logger.info('Backup targetpath: {}'.format(dest))
        create_path(path, logger, chdir=True)
    except:
        create_path(path, logger, chdir=True)


if __name__ == "__main__":
    download_package(logger)