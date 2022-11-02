from crypt import methods
import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt, unset_jwt_cookies, get_jwt_identity
from .DBmodel import Study, User, db

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
        access_token = create_access_token(identity=user.id, additional_claims = {"role":role})
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
            else:
                return view(**kwargs)
        return wrapped_view
    return decorator


def study_owner_required():
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
            study_id = kwargs["study_id"]
            current_user_id = get_jwt_identity()
            study = Study.query.filter_by(id=study_id, user_id=current_user_id).first()
            if study is None:
                return jsonify(errorMessage="User rights insufficient. You are not the study creater."), 401
            else:
                return view(study)
        return wrapped_view
    return decorator

def study_login_or_owner_required():
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
            study_id = kwargs["study_id"]
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            if "study_loggedin" in claims.keys() and study_id==claims["study_loggedin"]:
                study = Study.query.filter_by(id=claims["study_loggedin"]).first()
                errorMessage = "Your not logged into the study."
            else:
                study = Study.query.filter_by(id=study_id, user_id=current_user_id).first()
                errorMessage = "User rights insufficient. You are not the study creater."
            
            if study is None:
                return jsonify(errorMessage=errorMessage), 401
            else:
                return view(study)
        return wrapped_view
    return decorator
