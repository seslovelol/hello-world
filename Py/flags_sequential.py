# -*- coding: utf-8 -*-
import os
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
        res = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as e:
        res = e.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
        else:
            status = HTTPStatus.error
        msg = 'HTTP error {res.status_code} {res.reason}'.format(res=res)
    except requests.exceptions.ConnectionError:
        msg = 'Connect error'
        status = HTTPStatus.error
    else:
        msg = ''
        status = HTTPStatus.ok
        save_flag(res, cc+'.gif')
    if not verbose and msg:
        print('*** Error for {}: {}'.format(cc, msg))
    return Result(status, cc)

def download_many(base_url, cc_lst, verbose, req):
    counter = Counter()
    if verbose:
        cc_lst = tqdm.tqdm(cc_lst, len(cc_lst))
    for cc in cc_lst:
        result = download_one(base_url, cc, verbose)
        counter[result.status] += 1
    return counter

def main(download_many, default_req, max_req):
    base_url = SERVERS['DELAY']
    a_z = string.ascii_lowercase
    cc_all = sorted(a+b for a in a_z for b in a_z)
    req = min(default_req, max_req, len(cc_all))
    verbose = False
    t0 = timeit.default_timer()
    counter = download_many(base_url, cc_all, verbose, req)
    t1 = timeit.default_timer()
    if verbose:
        print('\n')
    for key, value in counter.items():
        print(key, ':', value)
    print(t1 - t0)

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
