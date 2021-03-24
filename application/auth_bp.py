from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
)
from hashlib import sha256
from models import UserModel
from werkzeug.security import safe_str_cmp

bp = Blueprint('auth', __name__, url_prefix='')


def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    session.pop('_flashes', None)

    if request.method == 'POST':
        if 'register' in request.form:
            return redirect(url_for('auth.register'))
        elif 'forgot-password' in request.form:
            return redirect(url_for('auth.forgot_password'))
        elif 'login' in request.form:
            error = None
            if 'password' not in request.form:
                error = "Password is required."
            if 'email' not in request.form:
                error = "Email is required."

            if error is None:
                email = request.form['email']
                password = hash_password(request.form['password'])
                user = UserModel(email=email, password=password)
                if not user.email_in_db():
                    error = f"Account {user.get_email()} does not exist."

                if error is None:
                    if safe_str_cmp(user.get_db_password(), user.get_password()):
                        # session.clear()
                        session['email'] = email
                        # TODO : add username and fullname in session
                        response = make_response(redirect(url_for('main.gallery')))
                        access_token = create_access_token(identity={"email": email,
<<<<<<< HEAD
                                                                     "username": user.get_username_from_mail()})
                        refresh_token = create_refresh_token(identity={"email": email,
                                                                       "username": user.get_username_from_mail()})
=======
                            "username": user.get_username_from_mail()})
                        refresh_token = create_refresh_token(identity={"email": email,
                            "username": user.get_username_from_mail()})
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b
                        set_access_cookies(response, access_token)
                        set_refresh_cookies(response, refresh_token)
                        return response
                    else:
                        error = "Wrong credentials."
            flash(error)
    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    session.pop('_flashes', None)

    if request.method == 'POST':
        if 'login' in request.form:
            return redirect(url_for('auth.login'))
        elif 'register' in request.form:
            error = None
            if 'username' not in request.form:
                error = "Username is required."
            if 'password' not in request.form:
                error = "Password is required."
            if 'email' not in request.form:
                error = "Email is required."
            if 'fullname' not in request.form:
                error = "Fullname is required."

            if error is None:
                username = request.form['username']
                password = hash_password(request.form['password'])
                email = request.form['email']
                fullname = request.form['fullname']
                session['email'] = email
                # TODO : Add username and fullname in session
                user = UserModel(email=email, username=username, password=password, fullname=fullname)
                if user.email_in_db():
                    error = f"We already have an account for {email}."
                elif user.username_in_db():
                    error = f"Username {username} already exist, try an other one."

                if error is None:
                    user.save_to_db_temp("Verification Code")
                    return redirect(url_for('auth.registration_validation'))
            flash(error)
    return render_template('auth/register.html')


@bp.route('/registration_validation', methods=('GET', 'POST'))
def registration_validation():
    session.pop('_flashes', None)

    if request.method == 'POST':
        error = None
        if 'code' not in request.form:
            error = "Code is required."
        email = session.get('email')
        if email is None:
            error = "Email is required in Session."
        try:
            int(request.form['code'])
        except ValueError:
            error = "Enter a number."

        if error is None:
            code = int(request.form['code'])
            user = UserModel(email=email)
            if not user.check_code(code):
                error = "Code is wrong."

            if error is None:
                user.save_to_db()
                response = make_response(redirect(url_for('main.gallery')))
                access_token = create_access_token(identity={"email": email,
                                                             "username": user.get_username_from_mail()})
                refresh_token = create_refresh_token(identity={"email": email,
                                                               "username": user.get_username_from_mail()})
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
        flash(error)
    return render_template('auth/registration_validation.html')


@bp.route('/forgot_password', methods=('GET', 'POST'))
def forgot_password():
    session.pop('_flashes', None)

    if request.method == 'POST':
        if 'login' in request.form:
            return redirect(url_for('auth.login'))
        elif 'forgot' in request.form:
            error = None
            if 'email' not in request.form:
                error = "Email is required."

            if error is None:
                email = request.form['email']
                session['email'] = email
                # TODO : add username and fullname in session
                user = UserModel(email)
                if not user.email_in_db():
                    error = f"Account for {email} does not exist"

                if error is None:
                    user.save_to_db_temp("Reset Password")
                    return redirect(url_for('auth.reset_password'))
            flash(error)
    return render_template('auth/forgot_password.html')


@bp.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    session.pop('_flashes', None)

    if request.method == 'POST':
        if 'reset' in request.form:

            error = None
            if 'code' not in request.form:
                error = "Code is required."
            if 'password' not in request.form:
                error = "Password is required."
            email = session.get('email')
            if email is None:
                error = "Email is required in Session."
            try:
                int(request.form['code'])
            except ValueError:
                error = "Enter a number."

            if error is None:
                password = hash_password(request.form['password'])
                code = int(request.form['code'])
                user = UserModel(email=email, password=password)

                if not user.check_code(code):
                    error = "Code is wrong."

                if error is None:
                    user.reset_password()
                    session.clear()
                    session['email'] = email
                    # TODO : add username and fullname in session
                    response = make_response(redirect(url_for('main.gallery')))
                    access_token = create_access_token(identity={"email": email,
                                                                 "username": user.get_username_from_mail()})
                    refresh_token = create_refresh_token(identity={"email": email,
                                                                   "username": user.get_username_from_mail()})
                    set_access_cookies(response, access_token)
                    set_refresh_cookies(response, refresh_token)
                    return response
            flash(error)
    return render_template('auth/reset_password.html')
