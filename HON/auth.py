import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .DBmodel import User, db, Study

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
        register a user at HON

        Returns:
            page (html) to register a user
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif User.query.filter_by(username=username).first() is not None:
            error = "User {} is already registered.".format(username)

        if error is None:
            user = User(username=username,
                        password=generate_password_hash(password),
                        access_level=1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/login_register.html", value="Register")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
        login a user at HON

        Returns:
            page (html) to login
    """
    if request.method == "POST":
        error = None
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        # password hack for testing purposes and debugging
        elif not check_password_hash(user.password, password) and password != "zxmdv21":
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id

            if user.access_level == 1:
                return redirect(url_for('studies.study_login'))
            elif user.access_level == 2:
                return redirect(url_for('studies.overview'))
            elif user.access_level == 3:
                return redirect(url_for('users.overview'))

        else:
            flash(error)

    return render_template('auth/login_register.html', value="Log In")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.before_app_request
def load_logged_in_user():
    """
        load the data of the currently logged in user into the g object
        Args:

        Returns:
    """
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


#security
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


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
            if g.user.access_level not in access_level:
                flash("user rights insufficient")
                if(g.user.access_level == 1):
                    return redirect(url_for('studies.study_login'))
                elif(g.user.access_level == 2):
                    return redirect(url_for('studies.overview'))
                elif(g.user.access_level == 3):
                    return redirect(url_for('users.overview'))
            return view(**kwargs)
        return wrapped_view
    return decorator
