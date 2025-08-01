import json

import requests
from flask import Blueprint, request, jsonify, render_template, url_for

accounts_app = Blueprint('accounts', __name__)


@accounts_app.route('/new-account')
def new_account():
    return render_template('new_account.html'), 200


@accounts_app.route('/create-new-account', methods=['POST'])
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
                "redirect_url": url_for('login.render_logged', login=accepted_data['login'])
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@accounts_app.route('/get-checking-account', methods=['POST'])
def get_checking_account():
    accepted_data = request.get_json()
    login = accepted_data['login']
    host = f"http://localhost:5000/api/clients/client?by_login=True&login={login}"
    client_response = requests.get(host)
    if client_response.status_code != 200:
        return jsonify({
            "status": "error",
            "message": "no user have been found"
        }), 500
    accounts = client_response.json()['data']['client']['accounts']
    checking_ids = [x['id'] for x in accounts if x['account_type'] == 'CHECKING']
    if len(checking_ids) > 0:
        return jsonify({
            "id": checking_ids[0],
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "no checking accound have been found"
        }), 500
