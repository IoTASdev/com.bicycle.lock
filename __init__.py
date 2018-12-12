from flask import Flask, request, jsonify
import user_auth
import stand

user = user_auth.User('NULL', 'NULL', 'NULL', 'NULL', 'NULL')

stand = stand.Stand('NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')

app = Flask(__name__)


@app.route('/')
def home():
    return 'I am on homepage'


@app.route('/provision/user', methods=['POST', 'GET'])
def provision_user():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            if request.headers['operation'] == 'create':
                data = request.json
                print(data['user_name'])
                response = user.register(data['user_name'], data['password'], data['mobile_no'], data['email_id'],
                                         data['timestamp'])
                if response['status'] == 'RES_CREATED':
                    return jsonify(response), 201
                else:
                    return jsonify(response), 400

            elif request.headers['operation'] == 'login':
                data = request.json
                response = user.login(data['mobile_no'], data['password'])
                if response['status'] == 'RES_OK':
                    return jsonify(response), 200
                else:
                    return jsonify(response), 400
        else:
            response = {'status': 'BAD_REQUEST', 'message': 'Not Supported Content Type'}
            return jsonify(response), 400


@app.route('/provision/stand', methods=['POST', 'GET'])
def provision_stand():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            if request.headers['operation'] == 'create':
                data = request.json
                response = stand.register(data['stand_name'], data['stand_coordinates'], data['stand_manager'], data['manager_contact'], data['no_of_bicycles'])
                if response['status'] == 'RES_CREATED':
                    return jsonify(response), 201
                else:
                    return jsonify(response), 400
        else:
            response = {'status': 'BAD_REQUEST', 'message': 'Not Supported Content Type'}
            return jsonify(response), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0')
