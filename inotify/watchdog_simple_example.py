#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Project: LearningPython
# Author: liuchundong <br>
# Date: 2019-7-25 <br>
# Time: 18:15 <br>
# Desc:

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO,
	                    format='%(asctime)s - %(message)s',
	                    datefmt='%Y-%m-%d %H:%M:%S')

	path = sys.argv[1] if len(sys.argv) > 1 else '.'
	event_handler = LoggingEventHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
