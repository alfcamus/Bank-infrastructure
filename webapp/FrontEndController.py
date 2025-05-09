from flask import Flask, render_template, request, url_for, jsonify
import requests
import logging

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
    login = request.args.get("login")
    host = f"http://localhost:5000/api/clients/client?by_login=True&login={login}"
    response = requests.get(host)
    accounts = response.json()['data']['client']['accounts']
    user = {
        "username": response.json()['data']['client']['name']
    }
    return render_template('logged.html', accounts = accounts, user = user), 200


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
                "redirect_url": url_for('logged', login = login_from_data)
            }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@front_app.route('/registration')
def registration():
    return render_template('registration.html'), 200


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
