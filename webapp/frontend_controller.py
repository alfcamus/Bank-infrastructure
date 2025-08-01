import logging

from flask import Flask, render_template, send_from_directory

from webapp.accounts import accounts_app
from webapp.home import home_app
from webapp.login import login_app
from webapp.registration import registration_app
from webapp.transfers import transfers_app

# Initialize Flask & register controllers
app = Flask(__name__, template_folder='template')
app.register_blueprint(home_app)
app.register_blueprint(login_app)
app.register_blueprint(registration_app)
app.register_blueprint(accounts_app)
app.register_blueprint(transfers_app)

FILES_DIR = "files"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/files/<path:filename>")
def get_file(filename):
    return send_from_directory(FILES_DIR, filename)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
