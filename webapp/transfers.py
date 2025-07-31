import base64
import json

import requests
from flask import Blueprint, request, jsonify, render_template, url_for

transfers_app = Blueprint('transfers', __name__)


@transfers_app.route('/transfer/own')
def own_transfer_render():
    user_token_based = request.cookies.get('user_token')
    user_token = base64.b64decode(user_token_based).decode('utf-8')
    user_token_json = json.loads(user_token)
    accounts = user_token_json['data']['client']['accounts']
    return render_template('own_transfer.html', accounts=accounts), 200


@transfers_app.route('/transfer/external')
def external_transfer():
    user_token_based = request.cookies.get('user_token')
    user_token = base64.b64decode(user_token_based).decode('utf-8')
    user_token_json = json.loads(user_token)
    accounts = user_token_json['data']['client']['accounts']
    return render_template('external_transfer.html', accounts=accounts), 200


@transfers_app.route('/make-transaction', methods=['POST'])
def make_transfer():
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
                if float(i["balance"]) < float(accepted_data["value"]):
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
        transaction_credit_response = requests.post(transaction_url, json=transaction_credit)
        transaction_debit_response = requests.post(transaction_url, json=transaction_debit)
        if transaction_credit_response.ok and transaction_debit_response.ok:
            return jsonify({
                "status": "success",
                "redirect_url": url_for('login.render_logged', login=user_token_json["data"]["client"]["login"])
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
