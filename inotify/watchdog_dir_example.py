#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2019-7-25 <br>
# Time: 18:15 <br>
# Desc:
import logging

import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

WATCH_PATH = 'D:\\usr\\shell'  # 监控目录

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='/usr/shell/watchdog_dir_example.log',
                    level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s-- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


class FileMonitorHandler(FileSystemEventHandler):
	def __init__(self, **kwargs):
		super(FileMonitorHandler, self).__init__(**kwargs)
		# 监控目录
		self._watch_path = WATCH_PATH

	def on_modified(self, event):
		if not event.is_directory:  # 文件改变都会触发文件夹变化
			file_path = event.src_path
			file_name = os.path.basename(file_path)
			print("文件改变全路径: %s, 文件名：%s" % (file_path, file_name))

	def on_moved(self, event):
		if not event.is_directory:  # 文件移动都会触发文件夹变化
			file_path = event.src_path
			print("文件移动: %s " % file_path)

	def on_created(self, event):
		if not event.is_directory:  # 文件改变都会触发文件夹变化
			file_path = event.src_path
			print("文件创建: %s " % file_path)

	def on_deleted(self, event):
		if not event.is_directory:  # 文件改变都会触发文件夹变化
			file_path = event.src_path
			print("文件删除: %s " % file_path)


if __name__ == "__main__":
	event_handler = FileMonitorHandler()
	observer = Observer()
	observer.schedule(event_handler, path=WATCH_PATH, recursive=True)  # recursive递归的
	observer.start()
	observer.join()
