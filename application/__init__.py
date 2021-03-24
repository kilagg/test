from flask import (
    Flask, Blueprint, flash, redirect, render_template, url_for
)
from flask_jwt_extended import (
    jwt_required
)


app = Flask(__name__,
            static_url_path='',
            static_folder='static')

from . import auth_bp
app.register_blueprint(auth_bp.bp)

from . import main_bp
app.register_blueprint(main_bp.bp)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def hello():
    return redirect(url_for('auth.register'))
