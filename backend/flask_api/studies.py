import os
import shutil
import json
from datetime import datetime
from flask import (
    Blueprint, request, jsonify, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from .auth import access_level_required, study_login_or_owner_required, study_owner_required
from .DBmodel import Study, Design, Imgset, db, Result, Scale, Tool, Study_stack, User_study_progress, Image
from sqlalchemy.orm import joinedload
from flask import send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token, create_refresh_token


bp = Blueprint("studies", __name__)


# study overview
@bp.route('/studies', methods =['GET'])
@jwt_required()
@access_level_required(["study_admin"])
def get_studies():
    """
        display all studies created by a user
        Args:

        Returns:
            study overview html
    """
    current_user_id = get_jwt_identity()
    studies = Study.query.filter_by(user_id=current_user_id).all()
    studies = [study.to_dict(include_imagesets=False) for study in studies]
    response = {}
    response["studies"] = studies
    return response

@bp.route('/study/<int:study_id>', methods=['GET'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
@study_login_or_owner_required()
def get_study(study):
    response = {}
    current_user_id = get_jwt_identity()
    results = Result.query.filter_by(study_id=study.id, user_id=current_user_id).all()
    study = study.to_dict(include_images=True,include_imagesets=True)
    study["results_current_user"] = [result.to_dict() for result in results]
    response["study"] = study
    return response    

@bp.route('/study', methods=['POST'])
@jwt_required()
@access_level_required(["study_admin"])
def create_study():
    response = {}
    error = None
    status_code = 200
    current_user_id = get_jwt_identity()

    study = Study()
    # save in db
    study.user_id = current_user_id
    default_password = ""
    study.password = generate_password_hash(default_password)
    # default design
    study.design = Design(study_id=study.id)
    study.design.get_defaults()
    db.session.add(study)
    db.session.commit()

    image_dir = study.get_image_dir()
    try:
        os.makedirs(image_dir)
    except:
        error = f"Error creating: {image_dir}"        
        response["error"] = error
        db.session.delete(study)
        db.session.commit()

    if error is None:
        response["study"] = study.to_dict(include_images=True,include_imagesets=True)
        return jsonify(response), 200
    else:
        return jsonify(response), 400


    
@bp.route('/study/<int:study_id>', methods=['PUT'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def update_study(study):
    """
        create/modify study
        Args:
            id: study_id
        Returns:
            study create html
    """
    response = {}
    error = None
    data = request.get_json()
    title = data["title"]
    password = data["password"]
    study_description = data["description"]    
    if study is None:
        error = "Study not found."

    if error is None:
        study.title = title
        if password:
            study.password = generate_password_hash(password)
        study.description = study_description
        study.updated = datetime.now().replace(microsecond=0)
        db.session.commit()
        status_code = 200
    else:
        response["error"] = error
        status_code = 404

    return jsonify(response), status_code


@bp.route('/study/<int:study_id>', methods=['DELETE'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def delete_study(study):
    """
        retrieve or delte study
        Args:
            id: study_id
        Returns:
            json object
    """
    response = {}
    error = None

    db.session.delete(study)
    db.session.commit()

    dir = os.path.join(current_app.config['IMAGE_PATH'],str(study.user_id), str(study.id))
    # remove image folder
    try:
        shutil.rmtree(dir)
    except:
        error = f"Error removing folder: {dir}"
        response["error"] = error

    if error is None:
        return jsonify(response), 200
    else:
        return jsonify(response), 400




@bp.route('/study/design/<int:study_id>', methods=['PUT'])
@jwt_required()
@study_owner_required()
def design(study):
    error = None
    design = request.get_json()

    # save design
    if study.design is None:
        study.design = Design(study_id=study_id)
    study.design.instructions = design["instructions"]
    study.design.button_labels = design["button_labels"]
    study.design.text_color = design["text_color"]
    study.design.background_color = design["background_color"]
    study.design.numb_img = design["numb_img"]
    study.design.numb_refimg = design["numb_refimg"]
    study.design.transition_time = design["transition_time"]
    study.design.show_viewport_info = design["show_viewport_info"]
    study.design.img_height = design["img_height"]
    study.design.img_height_auto = design["img_height_auto"]
    study.design.img_per_row = design["img_per_row"]
    study.design.numb_rois = design["numb_rois"]
    
    # delete old tools
    for tool in study.design.tools:
        db.session.delete(tool)
    for toolData in design["tools"]:
        tool = Tool.query.filter_by(
            cs_name=toolData["cs_name"], design_id=study.design.id).first()
        if tool is None:
            tool = Tool(design_id=study.design.id)
            db.session.add(tool)
        tool.cs_name = toolData["cs_name"]
        tool.key_binding = toolData["key_binding"]
        tool.settings = json.dumps(toolData["settings"])

    # delete old scales
    for scale in study.design.scales:
        db.session.delete(scale)
    for item in design["scales"]:
        scale = Scale(design_id=study.design.id)
        scale.text = item["text"]
        scale.min = item["min"]
        scale.max = item["max"]
        scale.type = item["type"]
        scale.labels = json.dumps(item["labels"])

        db.session.add(scale)

    db.session.commit()

    response = {}
    return jsonify(response)

#get image stack in cornerstone format
# @bp.route('/study/cs_stack/<int:study_id>/<image_ids>', methods=['GET'])
# @jwt_required()
# @access_level_required([2])
# def get_cs_stack(study_id,image_ids):
#     image_ids = [int(image_id) for image_id in image_ids.split("-")]
#     study = Study.query.filter_by(id=study_id).first()
#     cs_stack = study.get_cs_stack_by_imageIds(image_ids)
#     return cs_stack

#update select menus
# @bp.route('/study/get_cs_stacks/<int:study_id>/<group_info>', methods=['GET'])
# @jwt_required()
# @access_level_required(["study_participant","study_admin"])
# def get_cs_stacks(study_id,group_info):
#     study = Study.query.filter_by(id=study_id).first()
#     cs_stacks = study.images_to_cs_stacks(group_info)
#     response = {}
#     response["cs_stacks"] = cs_stacks
#     return response

@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['GET'])
@jwt_required()
@study_login_or_owner_required()
@access_level_required(["study_participant","study_admin"])
def get_imgset(study, position):
    imgset = Imgset.query.filter_by(study_id=study.id,position=position).first()
    error = None
    response = {}
    
    if imgset is None:
        error = "Imgset with position %s not found in study %s"%(position,study.title)
        response["error"] = error
        status_code = 404
    else:
        imgset_dict = imgset.to_dict()
        # info important for progressbar during study run
        response["study_length"] = len(study.imgsets)
        response["imgset"] = imgset_dict
        status_code = 200

    return jsonify(response), status_code


@bp.route('/study/imgset/<int:study_id>', methods=['POST'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def add_imgset(study):
    """
        add imageset
        Args:
            id: study_id
        Returns:
    """
    image_error = ""
    data = request.get_json()
    imgset_dict = data
    response = {}

    imgset = Imgset(study_id=study.id,position=imgset_dict["position"])
    if int(imgset_dict["position"]) <= len(study.imgsets):
        study.insert_imgset(imgset,imgset_dict["position"])

        # add stacks to imgset
        for stack in imgset_dict["stacks"]:
            study_stack = Study_stack(stack_id=stack["stack_id"],
                                      imgset_id=imgset.id,
                                      div_id=stack["div_id"],
                                      name=stack["name"],
                                      viewport=json.dumps(stack["viewport"]))
            if any(stack["tool_state"]):
                study_stack.tool_state = json.dumps(stack["tool_state"])
            if stack["segmentation_data"]:
                study_stack.seg_data = stack["segmentation_data"]

            db.session.add(study_stack)
        db.session.commit()

    response["error_msg"] = image_error
    response["imgset"] = imgset.to_dict()

    return jsonify(response)


@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['PUT'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def update_imgset(study, position):
    imgset = Imgset.query.filter_by(study_id=study.id,position=position).first()
    error = None
    data = request.get_json()
    imgset_dict = data
    response = {}
    if imgset is None:
        error = "Imgset with position %s not found in study %s"%(position,study.title)

    if error is None:
        # delete old images
        for stack_old in imgset.study_stacks:
            db.session.delete(stack_old)
            db.session.commit()

        # add images
        for stack in imgset_dict["stacks"]:
            study_stack = Study_stack(stack_id=stack["stack_id"],
                                      imgset_id=imgset.id,
                                      div_id=stack["div_id"],
                                      name=stack["name"],
                                      viewport=json.dumps(stack["viewport"]))
            if any(stack["tool_state"]):
                study_stack.tool_state = json.dumps(stack["tool_state"])
            if stack["segmentation_data"]:
                study_stack.seg_data = stack["segmentation_data"]

            db.session.add(study_stack)
        db.session.commit()
        response["error_msg"] = error
        response["imgset"] = imgset.to_dict()
        status_code = 200
    else:
        status_code = 404

    return jsonify(response), status_code


@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['DELETE'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def delete_imgset(study, position):
    response = {}
    imgset = Imgset.query.filter_by(study_id=study.id,position=position).first()
    if imgset is None:
        error = "Imgset with position %s not found in study %s"%(position,study.title)
        status_code = 404
        response["error_msg"] = error
    elif Result.query.filter_by(imgset_id=imgset.id).first():
        error = "Results are present for imgset %s! First delete results, then delete imgset."%(position)
        status_code = 409
        response["error_msg"] = error
    else:
        db.session.delete(imgset)
        db.session.commit()
        study.update_imgset_pos()
        status_code = 200

    return jsonify(response), status_code


@bp.route('/study/imgsets/<int:study_id>', methods=['GET'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def get_all_imgsets(study):
    #response
    response = {}
    imgsets = []
    for imgset in study.imgsets:
        imgsets.append(imgset.to_dict())
    response["imgsets"] = imgsets
    return jsonify(response)

@bp.route('/study/imgsets/<int:study_id>', methods=['POST'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def imgsets(study):
    image_error = ""
    #response
    response = {"imgsets":[]}
    imgsets_dict = request.get_json()
    for imgset_dict in imgsets_dict:
        imgset = Imgset(study_id=study.id,position=imgset_dict["position"])
        study.insert_imgset(imgset,imgset_dict["position"])

        # add stacks to imgset
        for stack in imgset_dict["stacks"]:
            study_stack = Study_stack(stack_id=stack["stack_id"],
                                      imgset_id=imgset.id,
                                      div_id=stack["div_id"],
                                      name=stack["name"],
                                      viewport=json.dumps(stack["viewport"]))
            if any(stack["tool_state"]):
                study_stack.tool_state = json.dumps(stack["tool_state"])
            if stack["segmentation_data"]:
                study_stack.seg_data = stack["segmentation_data"]

            db.session.add(study_stack)
        db.session.commit()
        response["imgsets"].append(imgset.to_dict())

    response["error_msg"] = image_error

    return jsonify(response)

# to do update function frontend and backend
# @bp.route('/study/imgsets/<int:study_id>', methods=['PUT'])
# @jwt_required()
# @access_level_required(["study_admin"])
# @study_owner_required()
# def upd_all_imgsets(study):
#     study = Study.query.filter_by(id=study_id).options(joinedload('imgsets')).first()

#     viewport_settings = request.get_json()
#     for imgset in study.imgsets:
#         for stack in imgset.study_stacks:
#             viewport_settings_old = json.loads(stack.viewport)
#             if viewport_settings["zoom"]:
#                 viewport_settings_old["scale"] = float(viewport_settings["zoom"])
#             if viewport_settings["pos_x"]:
#                 viewport_settings_old["translation"]["x"] = int(viewport_settings["pos_x"])
#             if viewport_settings["pos_y"]:
#                 viewport_settings_old["translation"]["y"] = int(viewport_settings["pos_y"])
#             if viewport_settings["ww"]:
#                 viewport_settings_old["voi"]["windowWidth"] = int(viewport_settings["ww"])
#             if viewport_settings["wc"]:
#                 viewport_settings_old["voi"]["windowCenter"] = int(viewport_settings["wc"])
#             stack.viewport = json.dumps(viewport_settings_old)
#     db.session.commit()

#     #response
#     response = {}
#     imgsets = []
#     for imgset in study.imgsets:
#         imgsets.append(imgset.to_dict())
#     response["imgsets"] = imgsets
#     return jsonify(response)


@bp.route('/study/imgsets/<int:study_id>', methods=['DELETE'])
@jwt_required()
@access_level_required(["study_admin"])
@study_owner_required()
def del_all_imgsets(study):
    response = {}
    study = Study.query.filter_by(id=study.id).options(joinedload('imgsets')).first()

    if Result.query.filter_by(study_id=study.id).first():
        error = "Results are present for this study! First delete results, then delete image sets."
        status_code = 409
        response = error
    else:
        status_code = 200
        for imgset in study.imgsets:
            db.session.delete(imgset)
        db.session.commit()

    return jsonify(response), status_code


# access study (login)
@bp.route('/study/login', methods=['POST'])
@jwt_required()
@access_level_required(["study_participant"])
def study_login():
    data = request.get_json()
    study_id = data['study_id']
    password = data['password']
    error = None
    response = {}
    study = Study.query.filter_by(id=study_id).first()
    user_id = get_jwt_identity()

    if study is None:
        error = 'Study not found.'
    elif not check_password_hash(study.password, password):
        error = 'Incorrect password.'

    if error is None:
        claims = get_jwt()
        role = claims["role"]
        access_token = create_access_token(identity=user_id, additional_claims = {"role":role, "study_loggedin": study_id})
        refresh_token = create_refresh_token(identity=user_id)
        response = jsonify(accessToken=access_token, refreshToken=refresh_token, role=role, study_loggedin=study_id)
        return response, 201        
        # response["study"] = study.to_dict(include_imagesets=True)
        # response["results"] = [result.to_dict() for result in results]
        # return response
    else:
        response["error"] = error
        return response, 404



# select stack, save selection and load next set
@bp.route('/study/result/<int:study_id>',  methods=['POST'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
@study_login_or_owner_required()
def save_result(study):
    error = None
    result_dict = request.get_json()
    imgset_id = result_dict["imgset_id"]
    current_user_id = get_jwt_identity()
    user_id = current_user_id
    result = Result.query.filter_by(imgset_id=imgset_id,
                                    user_id=user_id).first()

    if result is None:
        result = Result(user_id=user_id,
                        study_id=study.id,
                        imgset_id=imgset_id)
        if result_dict["scale_input"]:
            result.scale_input= json.dumps(result_dict["scale_input"])
        db.session.add(result)
        db.session.flush()
        picked_stack = Study_stack(stack_id=result_dict["picked_stack"]["stack_id"],
                                   result_id=result.id,
                                   div_id = result_dict["picked_stack"]["div_id"],
                                   name=result_dict["picked_stack"]["name"],
                                   viewport = json.dumps(result_dict["picked_stack"]["viewport"]))
        if any(result_dict["picked_stack"]["tool_state"]):
            picked_stack.tool_state = json.dumps(result_dict["picked_stack"]["tool_state"])
        if result_dict["picked_stack"]["segmentation_data"]:
            picked_stack.seg_data = result_dict["picked_stack"]["segmentation_data"]
        db.session.add(picked_stack)

        study_progress = User_study_progress.query.filter_by(study_id=study.id,
                                                             user_id=user_id).first()

        results_user = Result.query.filter_by(study_id=study.id,user_id=user_id).all()
        imgsets_finished = len(results_user)
        if study_progress is None:
            study_progress=User_study_progress(study_id=study.id,user_id=user_id,imgsets_finished=imgsets_finished)
            db.session.add(study_progress)
        else:
            study_progress.imgsets_finished=imgsets_finished

        db.session.commit()
    else:
        error = "Result was not saved. There is already a result for this user and image-set present. Please reload the page."

    # response
    response = {}
    response["error"] = error
    response["result"] = result.to_dict()    
    response["study_progress"] = study_progress.to_dict()

    return jsonify(response)


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')