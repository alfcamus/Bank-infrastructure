from flask import Flask, render_template
import logging

# Initialize Flask app
front_app = Flask(__name__, template_folder='template')
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Error handler
@front_app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    front_app.run(host='0.0.0.0', port=3000, debug=True)
