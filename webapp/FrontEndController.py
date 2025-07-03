from numbers import Number
from flask import Flask, render_template, request, url_for, jsonify
import requests
import logging
import base64
import json

# Initialize Flask app
front_app = Flask(__name__, template_folder='template')
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@front_app.route('/')
@front_app.route('/home')
def home():
    return render_template('home.html'), 200


@front_app.route('/logged')
def logged():
    user_token_based = request.cookies.get('user_token')
    if user_token_based is None:
        login = request.args.get("login")
        host = f"http://localhost:5000/api/clients/client?by_login=True&login={login}"
        client_response = requests.get(host)
        accounts = client_response.json()['data']['client']['accounts']
        user = {
            "username": client_response.json()['data']['client']['name']
        }
        user_token_b64 = base64.b64encode(json.dumps(client_response.json()).encode('utf-8'))
        return render_template('logged.html', accounts=accounts, user=user, user_token=user_token_b64.decode('utf-8')), 200
    else:
        user_token = base64.b64decode(user_token_based).decode('utf-8')
        user_token_json = json.loads(user_token)
        user = {
            "username": user_token_json['data']['client']['name']
        }
        accounts = user_token_json['data']['client']['accounts']
        return render_template('logged.html', accounts=accounts, user=user, user_token=user_token_based), 200

@front_app.route('/login', methods=['POST'])
def login():
    login_from_data = request.get_json()['login']
    password_from_data = request.get_json()['password']
    print(f'{login_from_data}, {password_from_data}')
    try:
        host = "http://localhost:5000/api/clients/client?check_password=True"
        response = requests.post(
            host,
            json={"login": login_from_data, "password": password_from_data}
        )
        if response.ok:
            return jsonify({
                "status": "success",
                "redirect_url": url_for('logged', login=login_from_data)
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@front_app.route('/registration')
def registration():
    return render_template('registration.html'), 200

@front_app.route('/transfer/own')
def own_transfer_render():
    user_token_based = request.cookies.get('user_token')
    user_token = base64.b64decode(user_token_based).decode('utf-8')
    user_token_json = json.loads(user_token)
    accounts = user_token_json['data']['client']['accounts']
    return render_template('own_transfer.html', accounts=accounts), 200

@front_app.route('/transfer/external')
def external_transfer():
    return render_template('external_transfer.html'), 200

@front_app.route('/new-account')
def new_account():
    return render_template('new_account.html'), 200


@front_app.route('/create-new-account', methods=['POST'])
def create_new_account():
    try:
        accepted_data = request.get_json()
        print(json.dumps(accepted_data))
        by_login_url = f"http://localhost:5000/api/clients/client?by_login=True&login={accepted_data['login']}"
        response_client = requests.get(by_login_url)
        id = response_client.json()['data']['client']['id']
        host = "http://localhost:5000/api/accounts/account"
        account_to_be_created = {
            'account_type': accepted_data['account_type'],
            'client_id': id,
            'balance': 0
        }
        response = requests.post(
            host,
            json=account_to_be_created)
        if response.ok:
            return jsonify({
                "status": "success",
                "redirect_url": url_for('logged')
                # TODO: retrieve login from response and send to 'frontend'
                # login: ...
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



@front_app.route('/own-transaction', methods=['POST'])
def own_transfer():
    try:
        accepted_data = request.get_json()
        user_token_based = request.cookies.get('user_token')
        user_token = base64.b64decode(user_token_based).decode('utf-8')
        user_token_json = json.loads(user_token)
        accounts = user_token_json["data"]["client"]["accounts"]
        for i in accounts:
            if i["id"] == accepted_data["source_account_id"]:
                print(i['balance'])
                print(accepted_data["value"])
                if Number(i["balance"]) < Number(accepted_data["value"]):
                    print("hej")
                    raise Exception("Not enough funds")
        print(json.dumps(accepted_data))
        transaction_url = "http://localhost:5000/api/transactions/transaction"
        transaction_credit = {
            "source_account": accepted_data["source_account_id"],
            "transfer_type": "CREDIT",
            "value": accepted_data["value"]
            }
        transaction_debit = {
            "source_account": accepted_data["target_account_id"],
            "transfer_type": "DEBIT",
            "value": accepted_data["value"]
            }
        transaction_credit_response = requests.post(transaction_url, json = transaction_credit)
        transaction_debit_response = requests.post(transaction_url, json = transaction_debit)
        if transaction_credit_response.ok and  transaction_debit_response.ok:
            return jsonify({
                "status": "success",
                "redirect_url": url_for('logged')
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@front_app.route('/register', methods=["POST"])
def register():
    try:
        accepted_data = request.get_json()
        host = "http://localhost:5000/api/clients/client"
        response = requests.post(
            host,
            json=accepted_data)
        if response.ok:
            return jsonify({
                "status": "success",
                "redirect_url": url_for('logged')
                # TODO: retrieve login from response and send to 'frontend'
                # login: ...
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Error handler
@front_app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


@front_app.errorhandler(500)
def server_error(error):
    return render_template('error.html'), 500


if __name__ == '__main__':
    front_app.run(host='0.0.0.0', port=3001, debug=True)
