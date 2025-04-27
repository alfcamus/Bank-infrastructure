from flask import Flask, render_template, request
import requests
import logging

# Initialize Flask app
front_app = Flask(__name__, template_folder='template')
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@front_app.route('/base')
def base_page():
    return render_template('base.html'), 200


@front_app.route('/login')
def login():
    return render_template('login.html'), 200


@front_app.route('/registration')
def registration():
    return render_template('registration.html'), 200

@front_app.route('/register', methods = ["POST"])
def register():
    accepted_data = request.get_json()
    host = "http://localhost:5000/api/clients/client"
    response = requests.post(
    host,
    json=accepted_data)
    return response

# Error handler
@front_app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    front_app.run(host='0.0.0.0', port=3001, debug=True)
