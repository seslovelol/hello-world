# -*- coding: utf-8 -*-
import os
import sys
import time
import tqdm
import string
import timeit
import requests
from enum import Enum
from collections import namedtuple, Counter

SERVERS = {
        'LOCAL': 'http://192.168.8.71:8001/flags',
        'DELAY': 'http://192.168.8.71:8002/flags',
        'ERROR': 'http://192.168.8.71:8003/flags',
}
Result = namedtuple('Result', 'status data')
HTTPStatus = Enum('Status', 'ok not_found error')
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
DEFAULT_SERVER = 'LOCAL'
DEST_DIR = r'C:\Users\seslo\Desktop\download'
MAX_CONCUR_REQ = 1
DEFAULT_CONCUR_REQ = 1

def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.content

def download_one(base_url, cc, verbose):
    try:
        img = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as e:
        res = e.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
            error_msg = 'HTTP error 404 - not find'
        else:
            status = HTTPStatus.error
            error_msg = 'HTTP error {res.status_code} - {res.reason}'.format(res)
    except requests.exceptions.ConnectionError as e:
        status = HTTPStatus.error
        error_msg = 'Connection error'
    else:
        save_flag(img, cc.lower()+'.gif')
        status = HTTPStatus.ok
        error_msg = ''
    if verbose and error_msg:
        print('*** Error for {}: {}'.format(cc, error_msg))
    return Result(status, cc)

def download_many(base_url, cc_lst, verbose, max_req):
    counter = Counter()
    cc_iter = sorted(cc_lst)
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:
        res = download_one(base_url, cc, verbose)
        status = res.status
        counter[status] += 1
    if not verbose:
        print(end='\n')
    return counter

def main(download_many, default_concur_req, max_concur_req):
    # cc_lst = sorted(POP20_CC)
    cc_set = set()
    a_z = string.ascii_lowercase
    cc_set.update(a+b for a in a_z for b in a_z)
    cc_lst = sorted(cc_set)
    actual_req = min(max_concur_req, len(cc_lst))
    base_url = SERVERS['DELAY']
    verbose = True
    t0 = timeit.default_timer()
    counter = download_many(base_url, cc_lst, verbose, actual_req)
    for key, value in counter.items():
        print(key, ':', value)
    print('Total:', sum(counter.values()))
    print(timeit.default_timer() - t0)

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
