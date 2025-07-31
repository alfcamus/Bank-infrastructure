import requests
from flask import Blueprint, request, jsonify, render_template, url_for

registration_app = Blueprint('registration', __name__)


@registration_app.route('/registration')
def render_registration():
    return render_template('registration.html'), 200


@registration_app.route('/register', methods=["POST"])
def register_client():
    try:
        accepted_data = request.get_json()
        host = "http://localhost:5000/api/clients/client"
        response = requests.post(
            host,
            json=accepted_data)
        if response.ok:
            return jsonify({
                "status": "success",
                "redirect_url": url_for('login.render_logged', login=response.json()['data']['login'])
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
