import redis
import json
import jwt

redis_client = connect = redis.Redis(host='localhost', port=6379, db=0) 


class User:
	def __init__(self, user_name, password, mobile_no, email_id, timestamp):
		self.user_name = 'NULL'
		self.password = 'NULL'
		self.mobile_no = 'NULL'
		self.email_id = 'NULL'
		self.timestamp = 'NULL'

	def register(self, user_name, password, mobile_no, email_id, timestamp, json_data):
		if redis_client.exists(mobile_no) == False:
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
			print(redis_client.hget(self.mobile_no, 'user_name'))
			response = {'status':'RES_CREATED', 'message':'User Created Succefully'}
			return response
		else:
			response = {'status':'BAD_REQUEST', 'message':'User already exists! Try with login'}
			return response

	def login(self, mobile_no, password):
		if redis_client.exists(mobile_no) == True:
			print(redis_client.hget(mobile_no,'password').decode("utf-8"))
			if redis_client.hget(mobile_no,'password').decode("utf-8") == password:
				message = {'mobile_no':mobile_no, 'password':password}
				encoded_data = jwt.encode(message , 'secret', algorithm='HS256')
				return {'message':'Logged In Successfully','status': 'RES_CREATED','Authorization':encoded_data.decode("utf-8")}
			else:
				return {'message':'Invalid Credentials','status': 'BAD_REQUEST'}
		else:
			return {'message':'User Does not exist','status': 'BAD_REQUEST'}
