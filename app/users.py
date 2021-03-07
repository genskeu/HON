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


@bp.route('/user/create', methods=["GET", "POST"], defaults={'id': None})
@bp.route('/user/modify/<int:id>', methods=["GET", "POST", "DELETE"])
@login_required
@access_level_required([3])
def user(id):
    user = User.query.filter_by(id=id).first()
    error = None

    # create new user or update exisiting one
    if request.method == "POST":
        # get form data from request
        username = request.form["username"]
        password = request.form["password"]
        access_level = int(request.form["access_level"])
        
        # create new user
        if user is None:
            # check if username and password were submitted and
            #       if the username already exists for another user
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
        # update user
        else:
            # check if the updated username already exists for another user
            if User.query.filter(User.username == username, User.id != id).first() is not None:
                error = "User {} is already registered.".format(username)

            if error is None:
                access_level_old = user.access_level
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

    # delete user
    if request.method == "DELETE":
        if user.access_level < 3:
            db.session.delete(user)
            db.session.commit()
            # if study admin delete folder in image dir
            path = os.path.join(current_app.config['IMAGE_PATH'],str(user.id))
            if user.access_level == 2 and os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                except:
                    print("Error removing folder: " + path)
        else:
            error = "Permission denied."
            flash(error)
        response = {}
        response["redirect"] = url_for("users.overview")
        return jsonify(response)
    if error:
        flash(error)
    return render_template("users/mk_md_user.html", user=user)


#change own username and generate_password
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
    return render_template("users/mk_md_user.html", user= user)
