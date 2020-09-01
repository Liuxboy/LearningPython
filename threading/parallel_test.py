import logging
import multiprocessing
import timeit
import operator
import aiomysql
# -*- coding: utf-8 -*-
import time
from multiprocessing.dummy import Pool as ThreadPool


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def process(item):
    log = get_logger(item)
    log.info("item: %s" % item)
    time.sleep(5)


def map():
    items = ['apple', 'bananan', 'cake', 'dumpling']
    # 串行处理
    start_1 = timeit.default_timer()
    for item in items:
        process(item)
    end_1 = timeit.default_timer()
    print("Serial cost time: {}s".format(end_1 - start_1))
    # 并行处理
    start_2 = timeit.default_timer()
    pool = ThreadPool()
    pool.map(process, items)
    pool.close()
    pool.join()
    end_2 = timeit.default_timer()
    print("Parallel time: {}s".format(end_2 - start_2))


def apply_async():
    items = ['apple', 'bananan', 'cake', 'dumpling']
    # 并行处理
    start_2 = timeit.default_timer()
    pool = ThreadPool()
    for item in items:
        pool.apply_async(process, (item,))
    pool.close()
    pool.join()
    end_2 = timeit.default_timer()
    print("Parallel time: {}s".format(end_2 - start_2))


def worker(a):
    print(a[1])


def exception_test():
    items = ([1, 2, 3], [2, 3], [3])
    pool = ThreadPool(processes=1)
    for item in items:
        pool.apply_async(worker, args=(item,)).get()
    pool.close()
    pool.join()
    print("Multiprocessing done!")


if __name__ == "__main__":
    exception_test()
