from flask import Blueprint, request, jsonify, current_app
from .auth import access_level_required
from .DBmodel import db, User
from werkzeug.security import generate_password_hash
import os
import shutil
from flask_jwt_extended import jwt_required

bp = Blueprint("users", __name__)

# user overview
@bp.route('/users')
@jwt_required()
@access_level_required(["user_admin"])
def overview():
    users = User.query.all()
    users = [user.to_dict() for user in users]
    return jsonify({"users": users})

# get and display data for a single user
# add default version
@bp.route('/user/<int:id>', methods=["GET"])
@jwt_required()
@access_level_required(["user_admin"])
def get_user(id):
    error = None
    user = User.query.filter_by(id=id).first()
    if user is None:
        error = f"User with id: {id} not found."

    if error is None:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"error_msg": error}), 404


# create a new user
@bp.route('/user', methods=["POST"])
@jwt_required()
@access_level_required(["user_admin"])
def create_user():
    error = None    
    # get form data from request
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    access_level = int(data["access_level"])
        
    # check if username and password were submitted and
    # if the username already exists for another user
    if not username:
        error = "Username is required."
    if not password:
        error = "Password is required."
    if User.query.filter_by(username=username).first() is not None:
        error = "User {} is already registered.".format(username)

    if error is None:
        user = User()
        user.username = username
        user.password = generate_password_hash(password)
        user.access_level = access_level
        db.session.add(user)
        db.session.commit()
        # if study admin create folder in image dir
        if user.access_level == 2:
            path = os.path.join(current_app.config['IMAGE_PATH'],str(user.id))
            try:
                os.makedirs(path)
            except:
                print(f"Could not create {path}.")
                return jsonify({"error_msg":"Could not create {path}."}), 400
            else:
                return jsonify({"user":user.to_dict()}), 200
    else:
        return jsonify({"error_msg": error}), 400



# edit an exisiting user
@bp.route('/user/<int:id>', methods=["PUT"])
@jwt_required()
@access_level_required(["user_admin"])
def modify_user(id):
    user = User.query.filter_by(id=id).first()
    error = None

    # get form data from request
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    access_level = int(data["access_level"])
        
 
    # check if the updated username already exists for another user
    if User.query.filter(User.username == username, User.id != id).first() is not None:
        error = "User {} is already registered.".format(username)

    if error is None:
        if user.access_level < 3:
            # only update attr which are not none or empty
            if username:
                user.username = username
            if password:
                user.password = generate_password_hash(password)
            user.access_level = access_level
            db.session.commit()
            # for study admin create folder in image dir 
            path = os.path.join(current_app.config['IMAGE_PATH'],str(user.id))
            if user.access_level == 2 and not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except:
                    print(f"Could not create {path}.")
                    return jsonify({"error_msg":"Could not create {path}."}), 400
                else:
                    return jsonify({"user":user.to_dict()}), 200
        else:
            error = "Permission denied." 
            return jsonify({"error_msg": error}), 401
    else:
        return jsonify({"error_msg": error}), 400



# delete user
@bp.route('/user/<int:id>', methods=["DELETE"])
@jwt_required()
@access_level_required(["user_admin"])
def delete_user(id):
    response = {}
    user = User.query.filter_by(id=id).first()
    # user admins can delete other user admins
    if user.access_level < 3:
        db.session.delete(user)
        db.session.commit()
        # if study admin delete folder in image dir
        path = os.path.join(current_app.config['IMAGE_PATH'],str(user.id))
        if user.access_level == 2 and os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except:
                print("Error removing folder while deleting user: " + path)
                response["error_msg"]="Error removing folder while deleting user: " + path
                return jsonify(response), 400
            else:
                return jsonify(response), 200
    else:
        error = "Permission denied."
        response["error_msg"] = error
        return jsonify(response),401

