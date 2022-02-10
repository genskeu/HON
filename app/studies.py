import os
import shutil
import json
from datetime import datetime
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for,
    jsonify, current_app, g, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from .auth import login_required, access_level_required
from .DBmodel import Study, Design, Imgset, db, Result, Scale, Tool, Image_stack, User_study_progress, Imgset_config, Image
from sqlalchemy.orm import joinedload

bp = Blueprint("studies", __name__)


# study overview
@bp.route('/')
@bp.route('/studies/overview')
@login_required
@access_level_required([2])
def overview():
    """
        display all studies created by a user
        Args:

        Returns:
            study overview html
    """
    studies = Study.query.filter_by(user_id=g.user.id).all()
    return render_template("studies/overview.html", studies=studies)


# create and modify studies
# should be seperated into html render and json api
@bp.route('/study/create', methods=['GET'], defaults={'id': None})
@bp.route('/study/update/<int:id>', methods=['GET'])
@login_required
@access_level_required([2])
def get_study(id):
    study = Study.query.filter_by(id=id).first()
    return render_template("studies/create.html", study=study)



@bp.route('/study', methods=['POST'])
@login_required
@access_level_required([2])
def create_study():
    response = {}
    error = None
    data = request.get_json()
    title = data["title"]
    password = data["password"]
    study_description = data["description"]

    # input validation
    if Study.query.filter_by(title=title,user_id=g.user.id).first() is not None:
        error = "Titel already used for a different study. Please choose a different study title."
    elif not title:
        error = "Title is required."
    elif not password:
        error = "Password is required."

    if error is None:
        study = Study()
        # save in db
        study.user_id = g.user.id
        study.title = title
        study.description = study_description
        study.password = generate_password_hash(password)
        db.session.add(study)
        db.session.commit()

        image_dir = study.get_image_dir()
        try:
            os.makedirs(image_dir)
        except:
            print("Error creating:" + image_dir)
        
        response["image_upload"] = url_for("studies.image_upload", study_id=study.id)
        response["study_design"] = url_for("studies.design", study_id=study.id)
        status_code = 200
    else:
        response["error"] = error
        status_code = 400

    return jsonify(response), status_code


@bp.route('/study/<int:id>', methods=['PUT'])
@login_required
@access_level_required([2])
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


    if Study.query.filter(Study.id!=id,Study.title==title,Study.user_id==g.user.id).first() is not None:
        error = "Titel already used for a different study. Please choose a different study title."

    if error is None:
        if title:
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
@login_required
@access_level_required([2])
def delete_study(id):
    """
        retrieve or delte study
        Args:
            id: study_id
        Returns:
            json object
    """
    study = Study.query.filter_by(id=id).first()

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
            print("Error removing folder: " + dir)
        response = {}
        response["redirect"] = url_for("studies.overview")
        return jsonify(response)



#render html file upload page
@bp.route('/study/files/<int:study_id>', methods=['GET'])
@login_required
@access_level_required([2])
def image_upload(study_id):
    study = Study.query.filter_by(id=study_id).first()
    return render_template("studies/image_upload.html", study=study)

# design for study html render
@bp.route('/study/design/<int:study_id>', methods=['GET'])
@login_required
@access_level_required([2])
def study_design(study_id):
    """
        create/modify, retrieve or delte study design
        Args:
            id: study_id
        Returns:
    """
    study = Study.query.filter_by(id=study_id).first()
    # default design
    if study.design is None:
        study.design = Design(study_id=study_id)
        study.design.get_defaults()
        db.session.commit()

    study.view = "study_admin"
    return render_template("studies/design.html",study=study)


# set design for study json API endpoint
@bp.route('/study/design/<int:study_id>', methods=['POST'])
@login_required
@access_level_required([2])
def design(study_id):
    study = Study.query.filter_by(id=study_id).first()

    if request.method == "POST":
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
        study.design.img_width = design["img_width"]
        study.design.img_height = design["img_height"]
        study.design.numb_rois = design["numb_rois"]
        for key, value in design["tools"].items():
            tool = Tool.query.filter_by(cs_name=key,design_id=study.design.id).first()
            if tool is None:
                tool = Tool(design_id=study.design.id)
                db.session.add(tool)
            tool.cs_name = key
            tool.label = value["label"]
            tool.key_binding = value["key_binding"]
            tool.status = value["status"]

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
        response["redirect"] = url_for('studies.overview')
        return jsonify(response)

#get image stack in cornerstone format
@bp.route('/study/cs_stack/<int:study_id>/<image_ids>', methods=['GET'])
@login_required
@access_level_required([2])
def get_cs_stack(study_id,image_ids):
    image_ids = [int(image_id) for image_id in image_ids.split("-")]
    study = Study.query.filter_by(id=study_id).first()
    cs_stack = study.get_cs_stack_by_imageIds(image_ids)
    return cs_stack

#update select menus
@bp.route('/study/get_cs_stacks/<int:study_id>/<group_info>', methods=['GET'])
@login_required
@access_level_required([1,2])
def get_cs_stacks(study_id,group_info):
    study = Study.query.filter_by(id=study_id).first()
    cs_stacks = study.images_to_cs_stacks(group_info)
    response = {}
    response["cs_stacks"] = cs_stacks
    return response

@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['GET'])
@login_required
@access_level_required([1,2])
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
@access_level_required([1,2])
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
@login_required
@access_level_required([1,2])
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
    elif user_study_progress.imgset.position+1 >= len(study.imgsets):
        error = "Error. You already participated and finished this study."
    elif user_study_progress and study.imgsets:
        imgset = Imgset.query.filter_by(study_id=study_id,
                                        position=user_study_progress.imgset.position+1).first()

    if error is not None:
        flash(error)
        return redirect(url_for('studies.study_login'))

    study.view="participant"
    return render_template('studies/design.html',
                           imgset=imgset,
                           study=study)


# select stack, save selection and load next set
@bp.route('/vote/<int:study_id>/<int:imgset_position>',  methods=['POST'])
@login_required
@access_level_required([1,2])
def vote(study_id, imgset_position):
    if request.method == "POST":
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
                    error = image_name + " not found part of study."
                else:
                    picked_stack.images.append(image)

            study_progress = User_study_progress.query.filter_by(study_id=study_id,
                                                                 user_id=user_id).first()

            if study_progress is None:
                study_progress=User_study_progress(study_id=study_id,user_id=user_id,imgset_id=imgset.id)
                db.session.add(study_progress)
            else:
                study_progress.imgset_id=imgset.id

            db.session.commit()

        # response
        response = {}
        next_imgset = Imgset.query.filter_by(
            study_id=study_id, position=imgset_position+1).first()
        if next_imgset is not None:
            response['imgset'] = next_imgset.to_dict()
            response['status'] = "ok"
            response['study_id'] = study_id
            response['user'] = user_id
            response['study_length'] = len(study.imgsets)
            response['transition_time'] = study.design.transition_time
        else:
            response['status'] = "done"
            response['study_length'] = len(study.imgsets)
        return jsonify(response)


from flask import send_from_directory

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')