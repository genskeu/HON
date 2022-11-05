from crypt import methods
from flask import Blueprint, jsonify, request, current_app, send_file, after_this_request
from .auth import access_level_required, study_owner_required, study_login_or_owner_required
import os
from .DBmodel import Result, Study, User, db, User_study_progress, Output
from sqlalchemy.orm import joinedload
import tarfile
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("results", __name__)

# get result by imgset_id
# @bp.route('/get_results_by_imgset_id/<imgset_id>')
# @jwt_required()
# @access_level_required(["study_admin"])
# def get_results_by_imgset_id(imgset_id):
#     results = Result.query.filter_by(imgset_id=imgset_id).join(User).add_column(User.username).add_column(Result.id).all()
#     response = {}
#     if results is None:
#         response["results"] = results
#     else:
#         response["results"] = [{"username" : result.username, "id":result.id} for result in results]
#     return response

# # get result by id
# @bp.route('/result/<id>', methods=["GET"])
# @jwt_required()
# @access_level_required(["study_admin"])
# def get_result(id):
#     result = Result.query.filter_by(id=id).first()
#     response = {}
#     response["result"] = result.to_dict()
#     return response


# get results by study for logged in user
@bp.route('/results/current_user/<int:study_id>', methods=["GET"])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
@study_login_or_owner_required()
def get_result_current_user(study):
    current_user_id = get_jwt_identity()
    user_id = current_user_id
    results = Result.query.filter_by(study_id=study.id, user_id=user_id).all()
    response = {}
    response["results"] = [result.to_dict() for result in results]
    return response


# delete results for user from study
@bp.route('/result/<study_id>/<user_id>', methods=['DELETE'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def delete_result(study,user_id):
    results = Result.query.filter_by(study_id=study.id,user_id=user_id).all()
    for result in results:
        db.session.delete(result)

    user_study_progress = User_study_progress.query.filter_by(study_id=study.id,user_id=user_id).first()
    db.session.delete(user_study_progress)
    db.session.commit()

    response = {}
    response["user_study_progress"] = User_study_progress.query.filter_by(study_id=study.id).all()
    response["user_study_progress"] = [usp.to_dict() for usp in response["user_study_progress"]]
    return jsonify(response)


# download csv file 
@bp.route('/results/<int:study_id>/download',methods=["GET"])
#@jwt_required()
#@access_level_required(["study_admin"])
def download_csv(study_id):
    filename = "results_study_%s.xlsx" % study_id
    filepath=os.path.join(current_app.config["IMAGE_PATH"],filename)
    @after_this_request
    def remove_file(response):
        try:
            os.remove(filepath)
        except Exception as error:
            print("Error removing downloaded results file handle", error)
        return response
    return send_file(filepath, filename, as_attachment=True)


# create csv file 
@bp.route('/results/<int:study_id>',methods=["GET"])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def create_csv(study):    
    results = Result.query.filter_by(study_id=study.id).options(joinedload('imgset'),
                                                                joinedload('imgset.study_stacks')).all()
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


@bp.route('/results/seg_data/<int:study_id>/download', methods=['GET'])
@jwt_required()
@access_level_required(["study_admin"])
def download_seg_data(study_id):
    study = Study.query.filter_by(id=study_id).first()
    tar_name = '%s_seg_masks.tar.gz'%study.title
    tar_path = os.path.join(study.get_image_dir(),tar_name)
    @after_this_request
    def remove_file(response):
        try:
            os.remove(tar_path)
        except Exception as error:
            print("Error removing downloaded segmentation file handle", error)
        return response

    return send_file(tar_path, tar_name, as_attachment=True)





@bp.route('/results/seg_data/<int:study_id>', methods=['GET'])
@jwt_required()
@access_level_required(["study_admin"])
def get_seg_data(study_id):
    study = Study.query.filter_by(id=study_id).first()
    results = Result.query.filter_by(study_id=study_id).all()

    # ground truth
    for imgset in study.imgsets:
        for stack in imgset.study_stacks:
            if stack.seg_data:
                file_name = "%s_%s_%s_gt.nii.gz"%(study.title,imgset.position,stack.name)
                file_path = os.path.join(study.get_image_dir(), file_name)
                stack.save_seg_data(file_path)
    
    # participant seg
    for result in results:
        stack_picked = result.stack_picked
        if stack_picked.seg_data:
            file_name = "%s_%s_%s_%s.nii.gz"%(study.title,result.imgset.position,stack_picked.name,result.user_id)
            file_path = os.path.join(study.get_image_dir(), file_name)
            result.stack_picked.save_seg_data(file_path)

    tar_name = '%s_seg_masks.tar.gz'%study.title
    tar_path = os.path.join(study.get_image_dir(),tar_name)
    tardir(study.get_image_dir(),tar_path, "nii.gz")

    response = {}
    return jsonify(response)




def tardir(path, tar_name, filter=None):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            if filter:
                files = [f for f in files if filter in f]
            for file in files:
                tar_handle.add(os.path.join(root, file),arcname=file)
                os.remove(os.path.join(root, file))

