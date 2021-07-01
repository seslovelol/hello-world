# -*- coding: utf-8 -*-
import os
import tqdm
import queue
import string
import timeit
import requests
import threading
from enum import Enum
from concurrent import futures
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
MAX_CONCUR_REQ = 1000
DEFAULT_CONCUR_REQ = 100
QUEUE = queue.Queue()

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
        else:
            status = HTTPStatus.error
        error_msg = 'HTTP error {res.status_code} - {res.reason}'.format(res=res)
    except requests.exceptions.ConnectionError:
        status = HTTPStatus.error
        error_msg = 'Connection error'
    else:
        save_flag(img, cc.lower()+'.gif')
        status = HTTPStatus.ok
        error_msg = ''
    if verbose and error_msg:
        print('*** Error for {}: {}'.format(cc, error_msg))
    # QUEUE.put(status)
    return Result(status, cc)

def download_many(base_url, cc_lst, verbose, max_req):
    counter = Counter()
    with futures.ThreadPoolExecutor(max_workers=max_req) as executor:
        to_do_map = {}
        for cc in cc_lst:
            future = executor.submit(download_one, base_url, cc, verbose)
            to_do_map[future] = cc
        done_iter = futures.as_completed(to_do_map)
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_lst))
        for future in done_iter:
            res = future.result()
            status = res.status
            counter[status] += 1
    # thread_lst = []
    # for cc in cc_iter:
    #     t = threading.Thread(target=download_one, args=(base_url, cc, verbose))
    #     thread_lst.append(t)
    #     t.start()
    # for t in thread_lst:
    #     res = t.join()
    # while not QUEUE.empty():
    #     status = QUEUE.get()
    #     counter[status] += 1
    return counter

def main(download_many, default_concur_req, max_concur_req):
    # cc_lst = sorted(POP20_CC)
    a_z = string.ascii_lowercase
    cc_all = sorted(a+b for a in a_z for b in a_z)
    actual_req = min(default_concur_req, max_concur_req, len(cc_all))
    base_url = SERVERS['DELAY']
    verbose = True
    t0 = timeit.default_timer()
    counter = download_many(base_url, cc_all, verbose, actual_req)
    t1 = timeit.default_timer()
    for key, value in counter.items():
        print(key, ':', value)
    print(t1 - t0)

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
