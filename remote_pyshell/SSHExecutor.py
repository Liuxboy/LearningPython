#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2019-7-31 <br>
# Time: 11:19 <br>
# Desc: 远程执行工具

import paramiko


def ssh_execute(_hostname, _username, _password, _command):
	ssh_client = paramiko.SSHClient()
	try:
		# 允许连接不在know_hosts文件中的主机。
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client.connect(hostname=_hostname, username=_username, password=_password)
		stdin, stdout, stderr = ssh_client.exec_command(command=_command)
		# 标准输入
		# print(stdin.readlines())
		# 标准错误
		if stderr.readlines():
			print(stderr.readlines())   # 标准错误
		# 标准输出
		for item in stdout.readlines():
			if 'grep' in item:
				continue
			print(item)
	except Exception as e:
		print('ssh %s@%s: %s' % (_username, _hostname, e))
		exit()
	finally:
		ssh_client.close()


if __name__ == "__main__":
	hostname = '192.168.37.131'
	username = 'root'
	password = 'root'
	cmd = "ls -l /home/xin/stock_att_tar"
	ssh_execute(hostname, username, password, cmd)
