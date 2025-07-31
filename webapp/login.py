import base64
import json

import requests
from flask import Blueprint, request, jsonify, render_template, url_for

login_app = Blueprint('login', __name__)


@login_app.route('/logged')
def render_logged():
    login = request.args.get("login")
    host = f"http://localhost:5000/api/clients/client?by_login=True&login={login}"
    client_response = requests.get(host)
    accounts = client_response.json()['data']['client']['accounts']
    user = {
        "username": client_response.json()['data']['client']['name']
    }
    user_token_b64 = base64.b64encode(json.dumps(client_response.json()).encode('utf-8'))
    return render_template('logged.html', accounts=accounts, user=user,
                           user_token=user_token_b64.decode('utf-8')), 200


@login_app.route('/login', methods=['POST'])
def login_client():
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
                "redirect_url": url_for('login.render_logged', login=login_from_data)
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
