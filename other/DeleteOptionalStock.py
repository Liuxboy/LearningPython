#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2018-5-29 <br>
# Time: 17:57 <br>
# Desc:


import demjson
import requests
import sys

sysNo = "CES110"


# 获取自选股票
def query(cid):
	url = "http://172.23.6.221/api/v1/portfolio/group/groupList"
	querystring = {
		"cid": cid,
		"sysNo": sysNo,
		"queryGroupType": "0"
	}
	headers = {
		'Cache-Control': "no-cache"
	}
	# print(querystring)
	response = requests.get(url, params=querystring, headers=headers)
	print(response.text)

	python_obj = demjson.decode(response.text, encoding="utf-8")
	result_set = python_obj['resultSet']
	grp_id = result_set[0]['grpId']
	stock_list = result_set[0]['stockList']
	symbol_list = ""
	for stock in stock_list:
		market = stock['market']
		stock_code = stock['symbol']
		symbol_list += market + '|' + stock_code + ","
	return symbol_list, grp_id


# 删除自选股
def delete(cid):
	url = "http://172.23.6.221/api/v1/portfolio/stock/delete"
	query_result = query(cid)
	symbol_list = query_result[0]
	grp_id = query_result[1]
	post_data = {
		"sysNo": sysNo,
		"cid": cid,
		"grpId": grp_id,
		"symbolList": symbol_list[:-1]
	}
	headers = {
		'Content-Type': "application/x-www-form-urlencoded",
		'Cache-Control': "no-cache",
	}
	# print(post_data)
	response = requests.post(url, data=post_data, headers=headers)
	print(response.text)


def main(cid, opt):
	if opt == "query":
		query(cid)
	else:
		delete(cid)


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])

