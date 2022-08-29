from crypt import methods
import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt, unset_jwt_cookies
from .DBmodel import User, db

jwt = JWTManager()

bp = Blueprint("auth", __name__, url_prefix="/auth")

# jwt auth by https://fareedidris.medium.com/cookie-based-authentication-using-flask-and-vue-js-part-1-c625a530c157
@bp.route("/register", methods=["POST"])
# @not_logged_in
def register():
    """
        register a user at HON

        Returns:
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    error = None
    response = jsonify()
    
    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."
    elif User.query.filter_by(username=username).first() is not None:
        error = f"User {username} is already registered."

    if error is None:
        user = User(username=username,
                    password=generate_password_hash(password),
                    access_level=1)
        db.session.add(user)
        db.session.commit()
        return response, 200
    else:
        
        return jsonify(message=error), 400


@bp.route("/login", methods=["POST"])
# @not_logged_in
def login():
    """
        login a user at HON

        Returns:
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    error = None

    user = User.query.filter_by(username=username).first()

    if user is None:
        error = 'Incorrect username.'
    # password hack for testing purposes and debugging
    elif not check_password_hash(user.password, password) and password != 'zxmdv21':
        error = 'Incorrect password. If you cant remember your password, please contact a user-admin.'

    if error is None:
        role = ""
        if user.access_level == 1:
            role = "study_participant"
        elif user.access_level == 2:
            role = "study_admin"
        elif user.access_level == 3:
            role = "user_admin"
        access_token = create_access_token(identity=user.id,additional_claims = {"role":role})
        refresh_token = create_refresh_token(identity=user.id)
        response = jsonify(accessToken=access_token, refreshToken=refresh_token, role=role)
        return response, 201
    else:
        return jsonify(errorMessage = error), 401



@bp.route('/logout', methods=["post"])
def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200


def access_level_required(access_level):
    """
        check if a user has sufficient user rights to access a certain view
        Args:
            access_level

        Returns:
            decorator
    """
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            claims = get_jwt()
            user_access_level = claims["role"]
            if user_access_level not in access_level:
                return jsonify(errorMessage="User rights insufficient."), 401
            return view(**kwargs)
        return wrapped_view
    return decorator

# @bp.before_app_request
# def load_logged_in_user():
#     """
#         load the data of the currently logged in user into the g object
#         Args:

#         Returns:
#     """
#     user_id = session.get("user_id")
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.filter_by(id=user_id).first()


# def not_logged_in(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is not None:
#             error = (f"You are already logged in as {g.user.username}."
#                      "You can't be logged in with multiple accounts using the same computer and browser or register a new user while logged in."
#                      "Please logout before logging in with another account or registering a new account.")
#             flash(error)
#             if g.user.access_level == 1:
#                 return redirect(url_for('studies.study_login'))
#             elif g.user.access_level == 2:
#                 return redirect(url_for('studies.overview'))
#             elif g.user.access_level == 3:
#                 return redirect(url_for('users.overview'))
#         return view(**kwargs)
#     return wrapped_view