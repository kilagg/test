from datetime import datetime, timedelta, timezone
from flask import redirect, url_for
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
    JWTManager,
<<<<<<< HEAD
    jwt_refresh_token_required,
    set_access_cookies
)
from flask_restful import Api
from models import RevokedTokenModel

from application import app
from resources.resources import (
    UploadDataOnSwarm,
    UserRegistration,
    UserRegistrationValidation,
    UserForgotPassword,
    UserForgotPasswordValidation,
    UserLogin,
    SecretResource
)
=======
    set_access_cookies
)
from flask_restful import Api

from application import app
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b

# Object of Api class
api = Api(app)

app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=12)

# JwtManager object
jwt = JWTManager(app)


@app.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_raw_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@jwt.expired_token_loader
@jwt.unauthorized_loader
def my_expired_token_callback(callback):
    return redirect(url_for('auth.login'))
<<<<<<< HEAD


@app.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {
               "message": f"New access_token",
               "access_token": access_token
           }, 200


# Checking that token is in blacklist or not
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):

    jti = decrypted_token['jti']

    return RevokedTokenModel(jti).save_to_db


api.add_resource(UploadDataOnSwarm, '/upload')
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserRegistrationValidation, '/registration-validation')
api.add_resource(UserForgotPassword, '/forgot-password')
api.add_resource(UserForgotPasswordValidation, '/forgot-password-validation')
api.add_resource(UserLogin, '/login')
api.add_resource(SecretResource, '/secret')

=======
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b
