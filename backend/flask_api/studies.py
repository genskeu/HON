from crypt import methods
import os
import shutil
import json
from datetime import datetime
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for,
    jsonify, current_app, g, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from .auth import access_level_required
from .DBmodel import Study, Design, Imgset, db, Result, Scale, Tool, Image_stack, User_study_progress, Imgset_config, Image
from sqlalchemy.orm import joinedload
from flask import send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity


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
        response["study"] = study.to_dict()
    except:
        error = f"Error creating: {image_dir}"        
        status_code = 400
        response["error"] = error
        db.session.delete(study)
        db.session.commit()

    return jsonify(response), status_code

@bp.route('/study/<int:id>', methods=['GET'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
def get_study(id):
    study = Study.query.filter_by(id=id).first()
    response = {}
    response["study"] = study.to_dict(include_images=True,include_imagesets=True)
    return response        


@bp.route('/study/<int:id>', methods=['PUT'])
@jwt_required()
@access_level_required(["study_admin"])
def update_study(id):
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
    study = Study.query.filter_by(id=id).first()
    current_user_id = get_jwt_identity()
    user_id = current_user_id
    if Study.query.filter(Study.id!=id,Study.title==title,Study.user_id==user_id).first() is not None:
        error = "Titel already used for a different study. Please choose a different study title."

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
        status_code = 400

    return jsonify(response), status_code


@bp.route('/study/<int:id>', methods=['DELETE'])
@jwt_required()
@access_level_required(["study_admin"])
def delete_study(id):
    """
        retrieve or delte study
        Args:
            id: study_id
        Returns:
            json object
    """
    study = Study.query.filter_by(id=id).first()
    response = {}
    error = None
    status_code = 200

    if request.method == "DELETE":
        for image in study.images:
            db.session.delete(image)
        db.session.delete(study)
        db.session.commit()

        dir = os.path.join(current_app.config['IMAGE_PATH'],str(study.user_id), str(study.id))
        # remove image folder
        try:
            shutil.rmtree(dir)
        except:
            error = f"Error removing folder: {dir}"
            response["error"] = error
            status_code = 400
        return jsonify(response), status_code



#render html file upload page
@bp.route('/study/files/<int:study_id>', methods=['GET'])
@jwt_required()
@access_level_required([2])
def image_upload(study_id):
    study = Study.query.filter_by(id=study_id).first()
    return render_template("studies/image_upload.html", study=study)



@bp.route('/study/design/<int:study_id>', methods=['PUT'])
@jwt_required()
def design(study_id):
    study = Study.query.filter_by(id=study_id).first()
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
    study.design.numb_rois = design["numb_rois"]
    for toolData in design["tools"]:
        tool = Tool.query.filter_by(
            cs_name=toolData["cs_name"], design_id=study.design.id).first()
        if tool is None:
            tool = Tool(design_id=study.design.id)
            db.session.add(tool)
        tool.cs_name = toolData["cs_name"]
        tool.key_binding = toolData["key_binding"]
        tool.settings = toolData["settings"]

    # delete old scales
    for scale in study.design.scales:
        db.session.delete(scale)
    for item in design["scales"]:
        scale = Scale(design_id=study.design.id)
        scale.text = item["text"]
        scale.min = item["min"]
        scale.max = item["max"]
        scale.type = item["type"]
        db.session.add(scale)

    db.session.commit()

    response = {}
    return jsonify(response)

#get image stack in cornerstone format
@bp.route('/study/cs_stack/<int:study_id>/<image_ids>', methods=['GET'])
@jwt_required()
@access_level_required([2])
def get_cs_stack(study_id,image_ids):
    image_ids = [int(image_id) for image_id in image_ids.split("-")]
    study = Study.query.filter_by(id=study_id).first()
    cs_stack = study.get_cs_stack_by_imageIds(image_ids)
    return cs_stack

#update select menus
@bp.route('/study/get_cs_stacks/<int:study_id>/<group_info>', methods=['GET'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
def get_cs_stacks(study_id,group_info):
    study = Study.query.filter_by(id=study_id).first()
    cs_stacks = study.images_to_cs_stacks(group_info)
    response = {}
    response["cs_stacks"] = cs_stacks
    return response

@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['GET'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
def get_imgset(study_id, position):
    imgset = Imgset.query.filter_by(study_id=study_id,position=position).first()
    study = Study.query.filter_by(id=study_id).first()
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

#retrieve, save, delete imgset API endpoint returning json
@bp.route('/study/imgset/<int:study_id>', methods=['POST'])
@jwt_required()
@access_level_required([2])
def add_imgset(study_id):
    """
        add imageset
        Args:
            id: study_id
        Returns:
    """
    study = Study.query.filter_by(id=study_id).first()
    image_error = ""
    data = request.get_json()
    imgset_dict = data["imgset"]
    response = {}

    imgset = Imgset(study_id=study_id,position=imgset_dict["position"])
    if int(imgset_dict["position"]) < len(study.imgsets):
        study.insert_imgset(imgset,imgset_dict["position"])
    db.session.add(imgset)
    db.session.commit()

    # add images
    for stack in imgset_dict["stacks"]:
        image_stack = Image_stack(imgset_id=imgset.id,
                                  div_id=stack["div_id"],
                                  name=stack["name"],
                                  viewport=json.dumps(stack["viewport"]))
        if any(stack["tool_state"]):
            image_stack.tool_state = json.dumps(stack["tool_state"])
        if stack["segmentation_data"]:
            image_stack.seg_data = stack["segmentation_data"]

        for image_name in stack["image_names"]:
            image = Image.query.filter_by(name=image_name,base_url=stack["base_url"]).first()
            if image is None:
                image_error += image_name + " not part of study %s."%study.title
            else:
                image_stack.images.append(image)
        db.session.add(image_stack)
    db.session.commit()

    response["error_msg"] = image_error
    return jsonify(response)


@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['PUT'])
@jwt_required()
@access_level_required([2])
def update_imgset(study_id, position):
    study = Study.query.filter_by(id=study_id).first()
    imgset = Imgset.query.filter_by(study_id=study_id,position=position).first()
    error = None
    image_error = ""
    data = request.get_json()
    imgset_dict = data["imgset"]
    response = {}
    if imgset is None:
        error = "Imgset with position %s not found in study %s"%(position,study.title)

    if error is None:
        data = request.get_json()
        imgset_dict = data["imgset"]
        # delete old images
        for stack_old in imgset.image_stacks:
            db.session.delete(stack_old)
            db.session.commit()

        # add images
        for stack in imgset_dict["stacks"]:
            image_stack = Image_stack(imgset_id=imgset.id,
                                      div_id=stack["div_id"],
                                      name=stack["name"],
                                      viewport=json.dumps(stack["viewport"]))
            if any(stack["tool_state"]):
                image_stack.tool_state = json.dumps(stack["tool_state"])
            if stack["segmentation_data"]:
                image_stack.seg_data = stack["segmentation_data"]

            for image_name in stack["image_names"]:
                image = Image.query.filter_by(name=image_name,base_url=stack["base_url"]).first()
                if image is None:
                    image_error += image_name + " not part of study %s."%study.title
                else:
                    image_stack.images.append(image)
            db.session.add(image_stack)
        db.session.commit()
        response["error_msg"] = image_error
        status_code = 200
    else:
        status_code =404

    return jsonify(response), status_code


@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['DELETE'])
@jwt_required()
@access_level_required([2])
def delete_imgset(study_id, position):
    response = {}
    study = Study.query.filter_by(id=study_id).first()
    imgset = Imgset.query.filter_by(study_id=study_id,position=position).first()
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



@bp.route('/study/imgsets/auto', methods=['POST'])
@jwt_required()
@access_level_required([2])
def random_imgsets():
    error = None
    data = request.get_json()
    study_id = data['study_id']
    study = Study.query.filter_by(id=study_id).options(joinedload('images')).first()
    config = Imgset_config(data)
    imgsets, ref_stack, error_image_stacks, error_imgsets = study.auto_create_imgsets(config)

    if error is error_image_stacks:
        # add imgsets to DB
        study_length=len(study.imgsets)

        for i, imgset_dict in enumerate(imgsets):
            imgset = Imgset(study_id=study.id,position=i+study_length)
            study.imgsets.append(imgset)
            for stack in imgset_dict:
                image_stack = Image_stack(imgset_id=imgset.id)
                image_stack.div_id = stack["div_id"]
                image_stack.name = stack["name"]
                image_stack.viewport = json.dumps(stack["viewport"])
                for image in stack["images"]:
                    image_stack.images.append(image)
                imgset.image_stacks.append(image_stack)

            for i in range(len(config.div_ids_ref)):
                image_stack_ref = Image_stack(imgset_id=imgset.id)
                image_stack_ref.div_id = config.div_ids_ref[i]
                image_stack_ref.name = ref_stack["name"]
                image_stack_ref.viewport = json.dumps(config.viewport_ref)
                with db.session.no_autoflush:
                    for img in ref_stack["images"]:
                        image = [image for image in study.images if image.name == img.name][0]
                        image_stack_ref.images.append(image)
                    imgset.image_stacks.append(image_stack_ref)

        db.session.commit()

    # response
    imgsets = []
    for imgset in study.imgsets:
        imgsets.append(imgset.to_dict())

    response = {}
    response["imgsets"] = imgsets
    response["error"] = error_image_stacks
    response["error_imgsets"] = error_imgsets
    return response



@bp.route('/study/imgsets/<int:study_id>', methods=['GET'])
@jwt_required()
@access_level_required([2])
def get_all_imgsets(study_id):
    study = Study.query.filter_by(id=study_id).options(joinedload('imgsets')).first()
    #response
    response = {}
    imgsets = []
    for imgset in study.imgsets:
        imgsets.append(imgset.to_dict())
    response["imgsets"] = imgsets
    return jsonify(response)

@bp.route('/study/imgsets/<int:study_id>', methods=['PUT'])
@jwt_required()
@access_level_required([2])
def upd_all_imgsets(study_id):
    study = Study.query.filter_by(id=study_id).options(joinedload('imgsets')).first()

    viewport_settings = request.get_json()
    for imgset in study.imgsets:
        for stack in imgset.image_stacks:
            viewport_settings_old = json.loads(stack.viewport)
            if viewport_settings["zoom"]:
                viewport_settings_old["scale"] = float(viewport_settings["zoom"])
            if viewport_settings["pos_x"]:
                viewport_settings_old["translation"]["x"] = int(viewport_settings["pos_x"])
            if viewport_settings["pos_y"]:
                viewport_settings_old["translation"]["y"] = int(viewport_settings["pos_y"])
            if viewport_settings["ww"]:
                viewport_settings_old["voi"]["windowWidth"] = int(viewport_settings["ww"])
            if viewport_settings["wc"]:
                viewport_settings_old["voi"]["windowCenter"] = int(viewport_settings["wc"])
            stack.viewport = json.dumps(viewport_settings_old)
    db.session.commit()

    #response
    response = {}
    imgsets = []
    for imgset in study.imgsets:
        imgsets.append(imgset.to_dict())
    response["imgsets"] = imgsets
    return jsonify(response)


@bp.route('/study/imgsets/<int:study_id>', methods=['DELETE'])
@jwt_required()
@access_level_required([2])
def del_all_imgsets(study_id):
    response = {}
    study = Study.query.filter_by(id=study_id).options(joinedload('imgsets')).first()

    if Result.query.filter_by(study_id=study_id).first():
        error = "Results are present for this study! First delete results, then delete imgsets."
        status_code = 409
        response["error_msg"] = error
    else:
        status_code = 200
        for imgset in study.imgsets:
            db.session.delete(imgset)
        db.session.commit()

    return jsonify(response), status_code


# access study (login)
@bp.route('/study/login', methods=['GET', 'POST'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
def study_login():
    if request.method == 'POST':
        study_id = request.form['study_id']
        password = request.form['password']
        error = None

        study = Study.query.filter_by(id=study_id).first()
        if study is None:
            error = 'Study not found.'
        # password hack for testing purposes and debugging
        elif not check_password_hash(study.password, password):
            error = 'Incorrect password.'

        if error is None:
            session['study_id'] = study.id
            return redirect(url_for('studies.study_run', study_id=study.id))

        flash(error)

    return render_template("auth/login_register.html", value="Access Study")


# run study
@bp.route('/study/run/<int:study_id>', methods=['GET'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
def study_run(study_id):
    if study_id != session.get("study_id"):
        return redirect(url_for('studies.study_login'))

    user_id = g.user.id
    study = Study.query.filter_by(id=study_id).first()
    user_study_progress = User_study_progress.query.filter_by(
        study_id=study_id,user_id=user_id).first()
    error = None

    # check if study has already been started by user
    if user_study_progress is None and study.imgsets:
        imgset = study.imgsets[0]
    elif user_study_progress is None and not study.imgsets:
        error = "Study is empty."
    elif user_study_progress.imgsets_finished == len(study.imgsets):
        error = "Error. You already participated and finished this study."
    elif user_study_progress and study.imgsets:
        # check for imgsets without result for this user
        results_user = Result.query.filter_by(study_id=study_id,user_id=user_id).all()
        results_user_imgset_ids = set([result.imgset.position for result in results_user])
        study_imgset_ids = set([imgset.position for imgset in study.imgsets])
        imgsets_left_ids = study_imgset_ids.difference(results_user_imgset_ids)
        imgsets_left_ids = list(imgsets_left_ids)
        imgsets_left_ids.sort()
        imgset = Imgset.query.filter_by(study_id=study_id,position=imgsets_left_ids[0]).first()

    if error is not None:
        flash(error)
        return redirect(url_for('studies.study_login'))

    study.view="participant"
    return render_template('studies/design.html',
                           imgset=imgset,
                           study=study,
                           user_study_progress=user_study_progress,
                           study_length=len(study.imgsets))


# select stack, save selection and load next set
@bp.route('/vote/<int:study_id>/<int:imgset_position>',  methods=['POST'])
@jwt_required()
@access_level_required(["study_participant","study_admin"])
def vote(study_id, imgset_position):
    error = None
    study = Study.query.filter_by(id=study_id).first()
    imgset = Imgset.query.filter_by(study_id=study_id,
                                    position=imgset_position).first()
    user_id = g.user.id
    result = Result.query.filter_by(imgset_id=imgset.id,
                                    user_id=user_id).first()

    if result is None:
        result_dict = request.get_json()
        result = Result(user_id=user_id,
                        study_id=study_id,
                        imgset_id=imgset.id)
        if result_dict["scale_input"]:
            result.scale_input= json.dumps(result_dict["scale_input"])
        db.session.add(result)
        db.session.flush()
        picked_stack = Image_stack(result_id=result.id,
                                   div_id = result_dict["picked_stack"]["div_id"],
                                   name=result_dict["picked_stack"]["name"],
                                   viewport = json.dumps(result_dict["picked_stack"]["viewport"]))
        if any(result_dict["picked_stack"]["tool_state"]):
            picked_stack.tool_state = json.dumps(result_dict["picked_stack"]["tool_state"])
        if result_dict["picked_stack"]["segmentation_data"]:
            picked_stack.seg_data = result_dict["picked_stack"]["segmentation_data"]
        db.session.add(picked_stack)
        for image_name in result_dict["picked_stack"]["image_names"]:
            image = Image.query.filter_by(name=image_name,base_url=result_dict["picked_stack"]["base_url"]).first()
            if image is None:
                error = f"Error saving results. Is {image_name} part of the study?"
            else:
                picked_stack.images.append(image)

        study_progress = User_study_progress.query.filter_by(study_id=study_id,
                                                             user_id=user_id).first()

        results_user = Result.query.filter_by(study_id=study_id,user_id=user_id).all()
        imgsets_finished = len(results_user)
        if study_progress is None:
            study_progress=User_study_progress(study_id=study_id,user_id=user_id,imgsets_finished=imgsets_finished)
            db.session.add(study_progress)
        else:
            study_progress.imgsets_finished=imgsets_finished

        db.session.commit()
    else:
        error = "Result was not saved. There is already a result for this user and image-set present. Please reload the page."

    # response
    response = {}
    response["error"] = error

    # check for imgsets without result for this user
    results_user = Result.query.filter_by(study_id=study_id,user_id=user_id).all()
    imgsets_finished = len(results_user)
    results_user_imgset_ids = set([result.imgset.position for result in results_user])
    study_imgset_ids = set([imgset.position for imgset in study.imgsets])
    imgsets_left_ids = study_imgset_ids.difference(results_user_imgset_ids)
    imgsets_left_ids = list(imgsets_left_ids)
    imgsets_left_ids.sort()
    if len(imgsets_left_ids):
        next_imgset = Imgset.query.filter_by(study_id=study_id,position=imgsets_left_ids[0]).first()
        response['imgset'] = next_imgset.to_dict()
        response['status'] = "ok"
        response['study_id'] = study_id
        response['user'] = user_id
        response['study_length'] = len(study.imgsets)
        response['transition_time'] = study.design.transition_time
        response['imgsets_finished'] = imgsets_finished
    else:
        response['status'] = "done"
        response['imgsets_finished'] = imgsets_finished
        response['study_length'] = len(study.imgsets)
    return jsonify(response)


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')