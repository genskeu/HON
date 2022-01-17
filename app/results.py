from flask import Blueprint, g, render_template, jsonify, request, url_for, current_app, send_from_directory, send_file
from .auth import login_required, access_level_required
import json
import csv
import os
import re
from .DBmodel import Length, Result, Study, User, db, EllipticalRoi,RectangleRoi,FreehandRoi, User_study_progress, Output
from sqlalchemy import func
from sqlalchemy.orm import lazyload, joinedload
from itertools import chain
import io
import ast

bp = Blueprint("results", __name__)

# get result by imgset_id
@bp.route('/get_results_by_imgset_id/<imgset_id>')
@login_required
@access_level_required([2])
def get_results_by_imgset_id(imgset_id):
    results = Result.query.filter_by(imgset_id=imgset_id).join(User).add_column(User.username).add_column(Result.id).all()
    response = {}
    if results is None:
        response["results"] = results
    else:
        response["results"] = [{"username" : result.username, "id":result.id} for result in results]
    return response

# get result by id
@bp.route('/result/<id>')
@login_required
@access_level_required([2])
def get_result(id):
    result = Result.query.filter_by(id=id).first()
    response = {}
    response["result"] = result.to_dict()
    return response


# results overview
@bp.route('/results/overview')
@login_required
@access_level_required([2])
def overview():
    studies = Study.query.filter_by(user_id=g.user.id).options(joinedload('user_study_progress',User_study_progress.user),
                                                               lazyload('imgsets'),
                                                               lazyload('imgsets.image_stacks')).all()

    return render_template("results/overview.html", studies=studies)


# retrieve or delete results for user from study
@bp.route('/result/<study_id>/<user_id>', methods=['GET','DELETE'])
@login_required
@access_level_required([2])
def delete_result(study_id,user_id):
    if request.method == "DELETE":
        results = Result.query.filter_by(study_id=study_id,user_id=user_id).all()
        for result in results:
            db.session.delete(result)

        user_study_progress = User_study_progress.query.filter_by(study_id=study_id,user_id=user_id).first()
        db.session.delete(user_study_progress)
        db.session.commit()

        response = {}
        response["redirect"] = url_for("results.overview")
        return jsonify(response)


# download csv file 
@bp.route('/results/download/<study_id>',methods=["GET"])
@login_required
@access_level_required([2])
def download_csv(study_id):
    filename = "results_study_%s.xlsx" % study_id
    filepath=os.path.join(current_app.config["IMAGE_PATH"],filename)
    return send_file(filepath, filename, as_attachment=True)


# create csv file 
@bp.route('/results/<study_id>',methods=["GET"])
@login_required
@access_level_required([2])
def create_csv(study_id):
    study = Study.query.filter_by(id=study_id).first()
    
    results = Result.query.filter_by(study_id=study_id).options(joinedload('imgset'),
                                                                joinedload('imgset.image_stacks')).all()
    users = User.query.all()
    inc_raw = "short"
    if request.args.get("include_raw_data"):
        inc_raw = True
    else: False
    if request.args.get("include_explanations"):
        inc_exp = True
    else:    
        inc_exp = False

    study.results = results    
    output_table = Output(study)
    output_table.get_data(users)
    output_table.save_table()

    resp = jsonify(success=True)
    return resp


