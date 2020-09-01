#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-03-21 <br>
# Time: 13:04 <br>
# Desc:

import asyncio
import time

import aiomysql


async def select_account(lp):
    i = 0
    sql_str = """SELECT * FROM ts_xd_account_info"""
    conn = await aiomysql.connect("127.0.0.1", "root", 'root', "edm_base", charset='utf8', loop=lp)
    async with aiomysql.cursors.SSCursor(conn) as cursor:
        await cursor.execute(sql_str)
        while True:
            row = await cursor.fetchone()
            if not row:
                break
            print(row)
            i += 1
    return i

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(select_account(loop))
    loop.close()
    end = time.time()
    print("cost time: {}s".format(end - start))
