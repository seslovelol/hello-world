# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Jul.29,2020'


import os
import sys
import time
import locale
import ftplib
import shutil
import socket
import random
import logging
import tarfile
import zipfile
import hashlib
import difflib
import platform
import threading
import subprocess
import logging.handlers


current_time = time.strftime('_%Y%m%d%H%M%S', time.localtime())
python_version = (float(platform.python_version()[:3]), float(platform.python_version()[4:]))
template_name = 'template.properties'
order_txt = 'order.txt'


def logger():
    """
        Define 2 handlers:
            handler1 is used to show messages in console.
            handler2 is used to write messages into log file.
    """
    # logging.basicConfig(
    #                 level    = logging.DEBUG,
    #                 format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    #                 datefmt  = '%Y-%m-%d %A %H:%M:%S',
    #                 filename = logFilename,
    #                 filemode = 'a')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    log_path = r'/home/deploytest/log'
    if not os.path.isdir(log_path):
        try:
            os.makedirs(log_path)
            print('Log path: {}'.format(log_path))
        except:
            print('Warning: Create log directory failed.')
    file_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, 'run.log'), when='W0', interval=1, backupCount=0)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def check_arglen(min, max, logger):
    """
        Check argument count.
    """
    length = len(sys.argv) - 1
    if length < min:
        logger.error('Too few arguments.')
        sys.exit(1)
    elif length > max:
        logger.error('Too much arguments.')
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


def check_file(file_name, logger):
    """
        Check file 3 times at most.
        Exit if it does not exists.
    """
    result = True
    for _ in range(3):
        if os.path.isfile(file_name):
            logger.debug('Find file {}'.format(file_name))
            result = False
            break
    if result:
        logger.error('NO such file {} in current dir {}'.format(file_name, os.getcwd()))
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
        logger.error('Failed to change to directory: {} '.format(path))
        sys.exit(1)


def check_path(path, logger, chdir=False):
    """
        Check path 3 times at most.
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
            break
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
        Return: tar | zip | other
    """
    file_suffix = file_name.split('.')[-1].lower()
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
        Get a package's namelist.
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
        Check a file's md5.
    """
    local_md5 = get_md5(file_name)
    md5_file = '.'.join((file_name, 'md5'))
    remote_md5 = read_file(md5_file, logger, exclude=True)[0]
    logger.info("Local file {}'s MD5 code: {}".format(file_name, local_md5))
    logger.info("Remote file {}'s value: {}".format(md5_file, remote_md5))
    if local_md5 == remote_md5:
        logger.info('MD5 codes are equal,data integrity.')
    else:
        logger.error('MD5 codes are different,data loss.')
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


def read_file(file_name, logger, exclude=False):
    """
        Read a file and return the file's content.
    """
    if os.path.isfile(file_name):
        try:
            file_reader = open(file_name, 'r')
            content = file_reader.read().splitlines()
        except:
            file_reader = open(file_name, 'r', encoding='utf-8-sig')
            content = file_reader.read().splitlines()
        finally:
            if exclude:
                # Remove the lines with '#' or the empty lines from content.
                [content.remove(t) for t in list(content) if t.startswith('#') or t == '']
                new_content = []
                for c in content:
                    new_content.append(c.strip())
                content = new_content
            file_reader.close()
    else:
        logger.error('No such file: {}'.format(file_name))
        sys.exit(1)
    return content


def extract_package(local, package_name, module, logger):
    """
        Extract files from a package.
    """
    suffix = get_suffix(package_name, logger)
    package_path = os.path.join(local, package_name)
    package, name_list = read_tar(package_path, logger) if suffix == 'tar' else read_zip(package_path, logger)
    change_path(local, logger)
    remove_path(os.path.join(local, module), logger)
    if suffix == 'tar' or suffix == 'zip' and python_version[1] > 5:
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
    elif suffix == 'zip' and python_version[1] < 6:
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
        Check module from a package.
        Exit if it does not exist.
    """
    name_list = get_namelist(local, package, logger)
    temp = '/'.join((package.split('.')[0], module))
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
    path = '/'.join((package.split('.')[0], module))
    change_path(local, logger)
    remove_path(path, logger)


def check_order(local, package, module, logger, extract=True):
    """
        Check order.txt from package/module.
        Extract it from package if it exists.
    """
    name_list = get_namelist(local, package, logger)
    order_path = '/'.join((package.split('.')[0], module, order_txt))
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
    template_path = '/'.join((package.split('.')[0], template_name))
    if template_path in name_list:
        logger.info('Find template file in package.')
    else:
        logger.error('No template file in package. Check your package.')
        sys.exit(1)
    if extract:
        extract_package(local, package, template_path, logger)
    return os.path.join(local, template_path)


def diff_file(file1, file2, output, logger):
    """
        Diff two files.
        Output: html.
    """
    text1_lines = read_file(file1, logger)
    text2_lines = read_file(file2, logger)
    diff = difflib.HtmlDiff()
    result = diff.make_file(text1_lines, text2_lines)
    with open(output, 'w') as file_writer:
        file_writer.writelines(result)
    logger.debug('Diff files done.')


def check_ftp(ftpinfo, logger):
    """
        Check ftp info.
    """
    if len(ftpinfo.split(':')) != 5:
        logger.error('Ftpinfo error: must be 5 arguments.')
        sys.exit(1)
    elif len(ftpinfo.split(':')[0].split('.')) != 4:
        logger.error('Ftpinfo error: ip error.')
        sys.exit(1)
    else:
        return ftpinfo.split(':')


def ftp_connect(host, port):
    """
        Create a ftp connection.
    """
    client = ftplib.FTP()
    try:
        client.connect(host, int(port))
        result = True
    except:
        result = False
    return client, result


def get_ftp(ftpinfo, logger, message=False):
    """
        Login ftp with the ftp connection.
        Return a ftp client for downloading or uploading files.
    """
    host, port, user, passwd, remote_dir = ftpinfo
    if message:
        logger.info('username = {}'.format(user))
        logger.info('password = ******')
        logger.info('host = {}'.format(host))
        logger.info('port = {}'.format(port))
    i = 0 
    while i < 10:
        client, result = ftp_connect(host, port)
        if result:
            break
        time.sleep(random.random() + 1)
        i += 1
        logger.info('{} Reconnect to {}:{}'.format(i, host, port))
    if not result:
        logger.error('Connect to {}:{} failed.'.format(host, port))
        sys.exit(1)
    try:
        client.login(user, passwd)
        logger.info('Connect to {}:{} successfully.'.format(host, port))
    except:
        logger.error('Login to {}:{} failed.'.format(host, port))
        sys.exit(1)
    return client


def ftp_cwd(client, remote, logger, mkdir=False):
    """
        Change remote directory of ftp server.
    """
    remote_list = list(filter(None, remote.replace('\\', '/').split('/')))
    remote_path = '/'.join((client.pwd(), '/'.join(remote_list)))
    if mkdir:
        remote_name = ''
        for name in remote_path.split('/'):
            remote_name += name + '/'
            try:
                client.cwd(remote_name)
                logger.debug('Change to remote directory: {} successfully.'.format(remote_name))
            except:
                try:
                    client.mkd(remote_name)
                    client.cwd(remote_name)
                    logger.debug('Create an change to remote directory: {} successfully.'.format(remote_name))
                except:
                    logger.error('Create remote directory: {} failed.'.format(remote_name))
                    sys.exit(1)
    else:
        try:
            client.cwd(remote_path)
            logger.debug('Change to remote directory: {} successfully.'.format(remote_path))
        except:
            logger.error('Change to remote directory: {} failed.'.format(remote_path))
            sys.exit(1)


def ftp_upload(client, file_name, logger):
    """
        Upload a file to ftp server.
    """
    local_file_size = os.stat(file_name).st_size
    result = False
    try:
        with open(file_name, 'rb') as local_file:
            client.storbinary('STOR {}'.format(os.path.basename(file_name)), local_file)
        remote_file_size = client.size(os.path.basename(file_name))
    except:
        logger.error('Upload {} to ftp failed.'.format(file_name))
        sys.exit(1)
    if local_file_size == remote_file_size:
        logger.debug('Upload {} to ftp successfully.'.format(file_name))
        result = True
    else:
        logger.debug('Remote file size: {} local file size {} , data loss.'.format(remote_file_size, local_file_size))
        logger.error('Upload {} to ftp failed.'.format(file_name))
        sys.exit(1)
    return result


def ftp_download(client, remote_file, logger):
    """
        Download a file from ftp server.
    """
    remote_list = client.nlst()
    result = False
    if remote_file in remote_list:
        remote_file_size = client.size(remote_file)
        try:
            with open(remote_file, 'wb') as local_file:
                client.retrbinary('RETR {}'.format(remote_file), local_file.write)
            local_file_size = os.stat(remote_file).st_size
            if remote_file_size == local_file_size:
                logger.info('Download file {} to {} successfully.'.format(remote_file, os.getcwd()))
                result = True
            else:
                logger.error('Remote file size: {} local file size {} , data loss.'.format(remote_file_size, local_file_size))
                os.remove(remote_file)
                logger.error('Download file {} to {} failed.'.format(remote_file, os.getcwd()))
        except:
            logger.error('Download file {} to {} failed.'.format(remote_file, os.getcwd()))
    else:
        logger.error('No such file {} in remote directory.'.format(remote_file))
    return result


def upload_log(package, module, ftpinfo, log_path, logger):
    """
        Upload a log file and show link of the file.
    """
    client = get_ftp(ftpinfo, logger)
    host = socket.gethostname()
    package_name = package.split('.')[0]
    remote_path = os.path.join(ftpinfo[4], 'log', package_name, module, host).replace('\\', '/')
    url = ''.join(('http://', ftpinfo[0]))
    ftp_cwd(client, remote_path, logger, mkdir=True)
    result = ftp_upload(client, log_path, logger)
    client.quit()
    if result:
        link = '/'.join((url, remote_path, os.path.basename(log_path)))
        logger.info(''.join(('log link: <a target="_blank" href="', link, '">', link, '</a>')))


def utf8_gbk(file_name):
    """
        Transfer charset from utf-8 to GBK.
    """
    file_reader = open(file_name, 'rb')
    try:
        content = file_reader.read().decode('utf-8').encode('gbk')
    except:
        file_reader.close()
    else:
        file_reader.close()
        with open(file_name, 'wb') as file_writer:
            file_writer.write(content)


def add_bom(file_name):
    """
        Add BOM head to a utf-8 file.
        Transfer charset from utf-8 to utf-8-bom.
    """
    BOM = b'\xef\xbb\xbf'
    exist_bom = lambda s: False if s == BOM else True
    file_reader = open(file_name, 'rb')
    content = file_reader.read()
    if exist_bom(file_reader.read(3)):
        with open(file_name, 'wb') as file_writer:
            file_writer.write(BOM)
            file_writer.write(content)
    file_reader.close()


def remove_bom(file_name):
    """
        Remove BOM head from a utf-8 file.
        Transfer charset from utf-8-bom to utf-8.
    """
    BOM = b'\xef\xbb\xbf'
    exist_bom = lambda s: True if s == BOM else False
    file_reader = open(file_name, 'rb')
    if exist_bom(file_reader.read(3)):
        content = file_reader.read()
        with open(file_name, 'wb') as file_writer:
            file_writer.write(content)
    file_reader.close()


def execute_script(path, logger):
    """
        Execute a script.
    """
    script_base = os.path.basename(path)
    script_dir = os.path.dirname(path)
    if os.path.isdir(script_dir):
        os.chdir(script_dir)
    suffix = get_suffix(script_base, logger, package=False)
    if suffix.lower() == 'bat':
        check_file(script_base, logger)
        remove_bom(script_base)
        utf8_gbk(script_base)
        returncode = sub_process(script_base, logger)
    elif suffix.lower() == 'sh':
        check_file(script_base, logger)
        script = ' '.join(('sh', script_base))
        returncode = sub_process(script, logger)
    elif suffix.lower() == 'py':
        check_file(script_base, logger)
        script = ' '.join(('python', script_base))
        returncode = sub_process(script, logger)
    else:
        returncode = sub_process(script_base, logger)
    if returncode == 0:
        logger.info('{} has executed successfully.'.format(script_base))
    else:
        logger.error('{} has failed to execute.'.format(script_base))
        sys.exit(1)


def stdout_process(process, logger):
    """
        Show process' output.
    """
    while True:
        line = process.stdout.readline().decode(locale.getpreferredencoding())
        if line:
            logger.info('{}'.format(line))
        else:
            break


def sub_process(command, logger):
    """
        Create a subprocess.
        Successfull: returncode = 0.
    """
    p = subprocess.Popen('{}'.format(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    t = threading.Thread(target=stdout_process, args=(p, logger))
    t.start()
    p.wait()
    t.join()
    return p.returncode


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