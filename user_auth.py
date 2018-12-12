import redis
import jwt

redis_client = connect = redis.Redis(host='localhost', port=6379, db=0)


class User:
	def __init__(self, user_name, password, mobile_no, email_id, timestamp):
		self.user_name = user_name
		self.password = password
		self.mobile_no = mobile_no
		self.email_id = email_id
		self.timestamp = timestamp

	def register(self, user_name, password, mobile_no, email_id, timestamp):
		print(redis_client.exists(mobile_no))
		if redis_client.exists(mobile_no) is 0:
			self.user_name = user_name
			self.password = password
			self.mobile_no = mobile_no
			self.email_id = email_id
			self.timestamp = timestamp
			user_data = {
						'consumer_type': 'user',
						'user_name': self.user_name,
						'password': self.password,
						'mobile_no': self.mobile_no,
						'email_id': self.email_id,
						'timestamp': self.timestamp
						}
			redis_client.hmset(self.mobile_no, user_data)
			print(redis_client.hget(self.mobile_no, 'user_name'))
			response = {'status': 'RES_CREATED', 'message': 'User Created Successfully'}
			return response
		else:
			response = {'status': 'BAD_REQUEST', 'message': 'User already exists! Try with login'}
			return response

	def login(self, mobile_no, password):
		if redis_client.exists(mobile_no) is 1:
			print(redis_client.hget(mobile_no, 'password').decode("utf-8"))
			if redis_client.hget(mobile_no, 'password').decode("utf-8") == password:
				message = {'mobile_no': mobile_no, 'password': password}
				encoded_data = jwt.encode(message, 'secret', algorithm='HS256')
				return {'message': 'Logged In Successfully', 'status': 'RES_OK', 'Authorization': encoded_data.decode("utf-8")}
			else:
				return {'message': 'Invalid Credentials', 'status': 'BAD_REQUEST'}
		else:
			return {'message': 'User Does not exist', 'status': 'BAD_REQUEST'}
