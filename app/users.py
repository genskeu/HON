from flask import (
    Blueprint, flash, redirect, request, render_template, url_for, g, jsonify, current_app
)
from .auth import login_required, access_level_required
from .DBmodel import db, User
from werkzeug.security import generate_password_hash
import os
import shutil

bp = Blueprint("users", __name__)

# user overview
@bp.route('/users/overview')
@login_required
@access_level_required([3])
def overview():
    users = User.query.all()
    return render_template("users/overview.html", users=users)

# get and display data for a single user
# add default version
@bp.route('/user/', defaults={'id': None}, methods = ['GET'])
@bp.route('/user/<id>', methods=["GET"])
@login_required
@access_level_required([3])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return render_template("users/mk_md_user.html", user=user)


# create a new user
@bp.route('/user/create', methods=["POST"])
@login_required
@access_level_required([3])
def create_user():
    error = None    
    # get form data from request
    username = request.form["username"]
    password = request.form["password"]
    access_level = int(request.form["access_level"])
        
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
        user.access_level = min(access_level,g.user.access_level)
        db.session.add(user)
        db.session.commit()
        # if study admin create folder in image dir
        if user.access_level == 2:
            path = os.path.join(current_app.config['IMAGE_PATH'],str(user.id))
            os.makedirs(path)
        return redirect(url_for('users.overview'))
    else:
        flash(error)
        return render_template("users/mk_md_user.html",user=None)



# edit an exisiting user
@bp.route('/user/modify/<int:id>', methods=["POST"])
@login_required
@access_level_required([3])
def modify_user(id):
    user = User.query.filter_by(id=id).first()
    error = None

    # get form data from request
    username = request.form["username"]
    password = request.form["password"]
    access_level = int(request.form["access_level"])
        
 
    # check if the updated username already exists for another user
    if User.query.filter(User.username == username, User.id != id).first() is not None:
        error = "User {} is already registered.".format(username)

    if error is None:
        if user.access_level < 3:
            # only update attr which are not none
            if username:
                user.username = username
            if password:
                user.password = generate_password_hash(password)
            user.access_level = access_level
            db.session.commit()
            # for study admin create folder in image dir 
            path = os.path.join(current_app.config['IMAGE_PATH'],str(user.id))
            if user.access_level == 2 and not os.path.isdir(path):
                os.makedirs(path)
            return redirect(url_for('users.overview'))
        else:
            error = "Permission denied." 
            flash(error)
    else:
        flash(error)
    return render_template("users/mk_md_user.html", user=user)



# delete user
@bp.route('/user/delete/<int:id>', methods=["DELETE"])
@login_required
@access_level_required([3])
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
        response["redirect"] = url_for("users.overview")
        return jsonify(response)
    else:
        error = "Permission denied."
        response["error"] = error
        return jsonify(response),401




#change own username and password
@bp.route('/profile', methods=["GET", "POST"])
@login_required
@access_level_required([1,2,3])
def profile():
    id = g.user.id
    user = User.query.filter_by(id=id).first()
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # check if the updated username already exists for other users
        if User.query.filter(User.username == username, User.id != id).first() is not None:
            error = "User {} is already registered.".format(username)

        if error is None:
            if username:
                user.username = username
            if password:
                user.password = generate_password_hash(password)
            db.session.commit()

        else:
            flash(error)
    return render_template("users/mk_md_user.html", user=user, profile=True)
