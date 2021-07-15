# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.31,2020'

import os
import sys
import psutil
import socket
import urllib.request
from lib.common import logger
from lib.common import check_arglen


def get_args():
    """
        Get arguments:
        Args: process, port, url.
    """
    length = check_arglen(1, 3)
    process, port, url = split_arg(sys.argv[1:])
    logger.info('Begin to execute {} {} {} {}'.format(
        os.path.join(os.getcwd(), sys.argv[0]), process, port, url
    ))
    return process, port, url


def split_arg(args):
    """
        Split arguments by '#', then split them by ','.
    """
    process, port, url = '', '', ''
    for arg in args:
        head = arg.split('#')[0]
        body = arg.split('#')[1].split(',')
        if head == 'process':
            process = body
        elif head == 'port':
            port = body
        elif head == 'url':
            url = body
        else:
            logger.error('Argument error: {}'.format(arg))
            sys.exit(1)
    for u in url:
        if not u.startswith(('http://', 'https://')):
            logger.error('URL must start with http:// or https://')
            sys.exit(1)
    return process, port, url


def check_port(port, count):
    """
        Check local machine;s port.
    """
    s = socket.socket()
    try:
        s.connect(('localhost', int(port)))
        s.close()
        logger.debug('{} is checked successfully.'.format(port))
        count += 1
    except:
        logger.debug('Failed to check {}'.format(port))
    return count


def check_process(process, count):
    """
        Check local machine's process.
    """
    temp = 0
    for p in psutil.process_iter():
        if p.pid in (os.getpid(), os.getppid()):
            pass
        elif process in p.name():
            temp += 1
    if temp > 0:
        count += 1
        logger.debug('{} is checked successfully.'.format(process))
    return count


def check_url(url, count):
    """
        Check url.
    """
    header = [('User-Agent', \
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44')]
    browser = urllib.request.build_opener()
    browser.addheaders = header
    try:
        browser.open(url)
        count += 1
        logger.debug('{} is opened successfully.'.format(url))
    except:
        logger.debug('Failed to open {}'.format(url))
    return count


def technical_check():
    process, port, url = get_args()
    process_total = len(process)
    port_total = len(port)
    url_total = len(url)
    process_count = 0
    port_count = 0
    url_count = 0
    for p in port:
        port_count = check_port(p, port_count)
    for p in process:
        process_count = check_process(p, process_count)
    for u in url:
        url_count = check_url(u, url_count)
    logger.info('Process total: {},count: {}'.format(process_total, process_count))
    logger.info('Port total: {},count: {}'.format(port_total, port_count))
    logger.info('Url total: {},count: {}'.format(url_total, url_count))
    if process_total == process_count and port_total == port_count and url_total == url_count:
        logger.info('Check done.')
        sys.exit(0)
    else:
        logger.error('Failed to check.')
        sys.exit(1)


if __name__ == "__main__":
    technical_check()