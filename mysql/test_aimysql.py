#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2020-03-21 <br>
# Time: 13:04 <br>
# Desc:


import asyncio
import aiomysql

db_host = "172.23.6.164"
port = 3366
user = "root"
password = "!QAZxsw2"
db_name = "account_analysis"


async def test_example(loop):
    conn = await aiomysql.connect(host=db_host,
                                  port=port,
                                  user=user,
                                  password=password,
                                  db=db_name,
                                  loop=loop)

    async with conn.cursor() as cur:
        await cur.execute("SELECT Host,User FROM user")
        print(cur.description)
        r = await cur.fetchall()
        print(r)
    conn.close()


async def test_example_execute(loop):
    conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                  user='root', password='root',
                                  db='test', loop=loop, autocommit=True)
    async with conn.cursor() as cur:
        await cur.execute("DROP TABLE IF EXISTS music_style;")
        await cur.execute("""
                            CREATE TABLE music_style
                            (id INT,
                            name VARCHAR(255),
                            PRIMARY KEY (id));
                          """)

        # insert 3 rows one by one
        await cur.execute("INSERT INTO music_style VALUES(1,'heavy metal')")
        await cur.execute("INSERT INTO music_style VALUES(2,'death metal');")
        await cur.execute("INSERT INTO music_style VALUES(3,'power metal');")
    conn.close()


if __name__ == "__main__":
    loops = asyncio.get_event_loop()
    loops.run_until_complete(test_example_execute(loops))
