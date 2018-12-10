
import redis
import json
import pickle

redis_client = connect = redis.Redis(host='localhost', port=6379, db=0) 


class User:
	def __init__(self, user_name, password, mobile_no, email_id, timestamp):
		self.user_name = 'NULL'
		self.password = 'NULL'
		self.mobile_no = 'NULL'
		self.email_id = 'NULL'
		self.timestamp = 'NULL'

	def register(self, user_name, password, mobile_no, email_id, timestamp, json_data):
		self.user_name = user_name
		self.password = password
		self.mobile_no = mobile_no
		self.email_id = email_id
		self.timestamp = timestamp
		srl_json_data = json.dumps(json_data)
		user_data = {
						'consumer_type':'user',
						'user_name':self.user_name,
						'password':self.password,
						'mobile_no':self.mobile_no,
						'email_id':self.email_id,
						'timestamp':self.timestamp
					}
		redis_client.hmset(self.mobile_no, user_data)
		#redis_client.hset(self.mobile_no, 'consumer_type','user')
		#redis_client.hset(self.mobile_no, 'user_name', self.user_name)
		#redis_client.hset(self.mobile_no, 'password', self.password)
		#redis_client.hset(self.mobile_no, 'mobile_no', self.mobile_no)
		#redis_client.hset(self.mobile_no, 'email_id', self.email_id)
		#redis_client.hset(self.mobile_no, 'timestamp', self.timestamp)
		print(redis_client.hget(self.mobile_no, 'user_name'))
		return 'user added succefully'

	def login(self, mobile_no, password):
		if redis_client.exists(mobile_no) == True:
			print(redis_client.hget(mobile_no,'password'))
			if redis_client.hget(mobile_no,'password') == password:
				return {'message':'Logged In Successfully','status': 'RES_CREATED'}
			else:
				return {'message':'Invalid Credentials','status': 'BAD_REQUEST'}
		else:
			return {'message':'User Does not exist','status': 'BAD_REQUEST'}
