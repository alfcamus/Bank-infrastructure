from flask import Blueprint, render_template

home_app = Blueprint('home', __name__)


@home_app.route('/')
@home_app.route('/home')
def home():
    return render_template('home.html'), 200
