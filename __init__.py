from flask import Flask, request, jsonify
import user_auth
import json

user = user_auth.User('NULL', 'NULL', 'NULL', 'NULL','NULL')

app = Flask(__name__)

@app.route('/')
def home():
    return 'I am on homepage'

@app.route('/provision', methods = ['POST','GET'])
def provision():
	if request.method == 'POST':
		if request.headers['Content-Type'] == 'application/json':
			if request.headers['operation'] == 'createUser':
				data = request.json
				print(data['user_name'])
				user.register(data['user_name'], data['password'], data['mobile_no'], data['email_id'], data['timestamp'], request.json)
				response = {'status': 'RES_CREATED', 'message':'User Created'}
				return jsonify(response),201
			elif request.headers['operation'] == 'loginUser':
				data = request.json
				response = user.login(data['mobile_no'], data['password']) 
				if response['status'] == 'RES_CREATED':
					return jsonify(response),201
				else:
					return jsonify(response),400
		else:
			response =  {'status': 'BAD_REQUEST', 'message':'Not Supported Content Type'}
			return jsonify(response),400

if __name__ == '__main__':
	app.run(host = '0.0.0.0')