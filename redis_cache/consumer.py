#!/usr/bin/env python   
# -*- coding:utf-8 -*-

import sys
import json
import redis
import argparse
sys.path.append('../')
from commons.macro import *
from tools.db_tools import save_json_data

class RedisConsumer(object):
	"""docstring for RedisConsumer"""
	def __init__(self, db=None, key=None, host='localhost', port=6379):
		super(RedisConsumer, self).__init__()
		# self.redis_connection = redis.StrictRedis(host=host, port=port, db=db if db else REDIS_DB_NUM)
		self.redis_connection = redis.StrictRedis(host=host, port=port)
		self.key = key if key else REDIS_LIST_KEY

	def start(self):
		while True:
			item=self.redis_connection.blpop(self.key)
			json_data = item[1]
			save_json_data(json_data)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='redis_consumer')
	parser.add_argument('--db', type=int, 
		help='redis db num', default=None)
	parser.add_argument('--key', type=str, 
		help='read list key', default=None)
	parser.add_argument('--host', type=str, 
		help='address list key', default='localhost')
	parser.add_argument('--port', type=int, 
		help='port to connect', default=6379)
	args = parser.parse_args()
	redis_consumer = RedisConsumer(args.db, args.key, args.host, args.port)
	try:
		redis_consumer.start()
	except KeyboardInterrupt:
		pass