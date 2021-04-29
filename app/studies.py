import os
import copy
import shutil
import json
import random
from datetime import datetime
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for,
    jsonify, current_app, g, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from .auth import login_required, access_level_required
from .DBmodel import Study, Design, Imgset, db, Result, Scale, Tool, Image_stack, FreehandRoi,User, RectangleRoi,EllipticalRoi, User_study_progress, Image
from shapely.geometry import Point, LineString, LinearRing, Polygon
from shapely.affinity import scale, rotate
from sqlalchemy.orm import lazyload, joinedload, subqueryload

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
@bp.route('/study/create', methods=['GET','POST'], defaults={'id': None})
@bp.route('/study/modify/<int:id>', methods=['GET','POST'])
@login_required
@access_level_required([2])
def create_modify_study(id):
    """
        create/modify study
        Args:
            id: study_id
        Returns:
            study create html
    """
    study = Study.query.filter_by(id=id).first()
    error = None

    # create new study or update exisiting one
    if request.method == 'POST':
        title = request.form["title"]
        password = request.form["password"]
        study_description = request.form["description"]

        # create new study
        if study is None:

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

        # update existing study
        else:
            if Study.query.filter(Study.id!=id,Study.title==title,Study.user_id==g.user.id).first() is not None:
                error = "Titel already used for a different study. Please choose a different study title."

            if error is None:
                study.user_id = g.user.id
                if title:
                    study.title = title
                if password:
                    study.password = generate_password_hash(password)
                study.description = study_description
                study.updated = datetime.now().replace(microsecond=0)
                db.session.commit()

        # redirect
        if error is None:
            if "image_upload" in request.form.keys():
                return redirect(url_for('studies.image_upload', study_id=study.id))
            else:
                return redirect(url_for('studies.study_design', study_id=study.id))

        # flash errors
        flash(error)

    return render_template("studies/create.html", study=study)


# (retrieve and) delete studies API endpoints returning json objects
@bp.route('/study/<int:id>', methods=['DELETE'])
@login_required
@access_level_required([2])
def study(id):
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

#retrieve, save, delete imgset API endpoint returning json
@bp.route('/study/imgset/<int:study_id>', methods=['POST'], defaults={'position':None})
@bp.route('/study/imgset/<int:study_id>/<int:position>', methods=['GET','PUT','DELETE'])
@login_required
@access_level_required([1,2])
def imgset(study_id, position):
    """
        create/modify, retrieve or delte imageset
        Args:
            id: study_id
        Returns:
    """
    imgset = Imgset.query.filter_by(study_id=study_id,position=position).first()
    study = Study.query.filter_by(id=study_id).first()
    data = request.get_json()
    error = None
    status_code = 200
    
    if data:
        imgset_dict = data["imgset"]

    response = {}
    if request.method == "GET":
        if imgset is None:
            error = "Imgset not found"

        if error is None:
            imgset_dict = imgset.to_dict()
            # info important for progressbar during study run
            response["study_length"] = len(study.imgsets)
            response["imgset"] = imgset_dict

    if request.method == "POST" and g.user.access_level == 2:
        imgset = Imgset(study_id=study_id,position=imgset_dict["position"])
        study.insert_imgset(imgset,imgset_dict["position"])
        db.session.add(imgset)
        db.session.commit()

    if request.method == "PUT" and g.user.access_level == 2:
        if imgset is None:
            error = "Imgset not found"

        if error is None:
            data = request.get_json()
            imgset_dict = data["imgset"]
            # delete old images
            for stack_old in imgset.image_stacks:
                db.session.delete(stack_old)
                db.session.commit()

    if request.method in ["POST","PUT"] and g.user.access_level == 2:
        # add images
        for stack in imgset_dict["stacks"]:
            image_stack = Image_stack(imgset_id=imgset.id,
                                      div_id=stack["div_id"],
                                      name=stack["name"],
                                      viewport=json.dumps(stack["viewport"]))
            if any(stack["tool_state"]):
                image_stack.tool_state = json.dumps(stack["tool_state"])
            for image_name in stack["image_names"]:
                image = [image for image in study.images if image.name == image_name]
                if image == []:
                    error = image_name + " not found part of study."
                else:
                    image_stack.images.append(image[0])
            db.session.add(image_stack)
        db.session.commit()

    if request.method == "DELETE" and g.user.access_level == 2:
        if imgset is None:
            error = "Imgset not found"
        else:
            db.session.delete(imgset)
            db.session.commit()
            study.update_imgset_pos()

    if error:
        response["error"] = error
        status_code = 404
    return jsonify(response), status_code


#auto create imgsets
def create_AFC_imgsets(stacks, pos_pattern, neg_pattern, div_ids, order):
    imgset_size = len(div_ids)
    error = ""
    pos_stacks = []
    neg_stacks = []
    for stack in stacks:
        stack_info = stack["name"].split("_")
        if len(stack_info) < 3:
            error += stack["name"] + ": wrong naming scheme." + "\n"
        elif pos_pattern == stack_info[1]:
            pos_stacks.append(stack)
        elif neg_pattern == stack_info[1]:
            neg_stacks.append(stack)
        else:
            error += stack["name"] + ": group info not found." + "\n"
    if order == "ordered":
        pos_stacks.sort(key=lambda pos_stack: int(pos_stack["name"].split("_")[0]))
    else:
        random.shuffle(pos_stacks)
    imgsets = []
    for pos_stack in pos_stacks:
        imgset = []
        pos_stack_info = pos_stack["name"].split("_")
        group_info = pos_stack_info[2]
        neg_stacks_group = [neg_stack for neg_stack in neg_stacks if group_info == neg_stack["name"].split("_")[2]]
        if len(neg_stacks_group) < (imgset_size-1):
            error += "Not enough negative images found for " + pos_stack["name"] + "\n"
            continue
        # pick neg images
        for rand_int in random.sample(range(len(neg_stacks_group)), imgset_size-1):
            imgset.append(copy.deepcopy(neg_stacks_group[rand_int]))
        # add pos stack
        imgset.insert(random.randint(0,imgset_size),pos_stack)
        for i in range(imgset_size):
            imgset[i]["div_id"] = div_ids[i]
        imgsets.append(imgset)
    return imgsets,error


def create_ROClike_imgsets(stacks, div_ids, order):
    imgset_size = len(div_ids)
    if order == "random":
        random.shuffle(stacks)
    else:
        stacks.sort(key=lambda stack: stack["name"].split("_")[0])
    imgsets = []
    error = None
    for i in range(0,len(stacks) - imgset_size + 1, imgset_size):
        imgset = stacks[i:i+imgset_size]
        for i, stack in enumerate(imgset):
            stack["div_id"] = div_ids[i]
        imgsets.append(imgset)

    if order == "random":
        random.shuffle(imgsets)

    return imgsets,error


@bp.route('/study/imgsets/auto', methods=['POST'])
@login_required
@access_level_required([2])
def random_imgsets():
    error = None
    data = request.get_json()
    study_id = data['study_id']
    study = Study.query.filter_by(id=study_id).options(joinedload('images')).first()
    # pattern
    pos_pattern = data['pos_pattern']
    neg_pattern = data['neg_pattern']
    # settings
    ref_stack_name = data['ref_stack_name']
    div_ids = data["div_ids"]
    div_ids_ref = data["div_ids_ref"]
    # viewport
    viewport = data['viewport']
    viewport_ref = data['viewport_ref']
    imgset_type = data['imgset_type']
    order = data["order"]
    grouping_info = data["stackmode"]

    # build stacks from images
    image_stacks = {}
    study.images.sort(key=lambda image: image.name)
    for image in study.images:
        if grouping_info == "single_images":
            stack_name = image.name
        else:
            stack_name = "_".join(image.name.split("_")[0:3])

        if stack_name in image_stacks:
            image_stacks[stack_name]["image_names"].append(image.name)
        else:
            image_stacks[stack_name] = {}
            image_stacks[stack_name]["name"] = stack_name
            image_stacks[stack_name]["viewport"] = viewport
            image_stacks[stack_name]["image_names"] = [image.name]

    if ref_stack_name in image_stacks.keys():
        ref_stack = image_stacks[ref_stack_name]
    elif ref_stack_name != "" and ref_stack_name not in image_stacks.keys():
        error = "Error creating the reference stack: " + ref_stack_name + "."
    elif ref_stack_name == "" and div_ids_ref:
        error = "No reference stack specified, but the number of reference images (general settings) is not 0."
    image_stacks = [image_stacks[stack_name] for stack_name in image_stacks if stack_name != ref_stack_name]

    # create imgsets
    if imgset_type == "afc":
        imgsets,error_imgsets  = create_AFC_imgsets(image_stacks,pos_pattern,neg_pattern,div_ids,order)
    elif imgset_type == "standard":
        imgsets,error_imgsets = create_ROClike_imgsets(image_stacks,div_ids,order)

    if error is None:
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
                with db.session.no_autoflush:
                    for image_name in stack["image_names"]:
                        image = Image.query.filter_by(name=image_name).first()
                        image_stack.images.append(image)
                    imgset.image_stacks.append(image_stack)

            for i in range(len(div_ids_ref)):
                image_stack_ref = Image_stack(imgset_id=imgset.id)
                image_stack_ref.div_id = div_ids_ref[i]
                image_stack_ref.name = ref_stack["name"]
                image_stack_ref.viewport = json.dumps(viewport_ref)
                with db.session.no_autoflush:
                    for image_name in ref_stack["image_names"]:
                        image = Image.query.filter_by(name=image_name).first()
                        image_stack_ref.images.append(image)
                    imgset.image_stacks.append(image_stack_ref)

        db.session.commit()

    # response
    imgsets = []
    for imgset in study.imgsets:
        imgsets.append(imgset.to_dict())

    response = {}
    response["imgsets"] = imgsets
    response["error"] = error
    response["error_imgsets"] = error_imgsets
    return response

# randomize imgset order of exisiting study
@bp.route('/study/randomize/<int:study_id>', methods=['POST'])
@login_required
@access_level_required([2])
def randomize(study_id):
    study = Study.query.filter_by(id=study_id).first()
    study.shuffle_imgsets()
    #study.update_imgset_pos()
    imgsets = []
    for imgset in study.imgsets:
        imgsets.append(imgset.to_dict())

    response = {}
    response["imgsets"] = imgsets
    return jsonify(response)

#get, delete or update all imgsets
@bp.route('/study/imgsets/<int:study_id>', methods=['GET','DELETE','PUT'])
@login_required
@access_level_required([2])
def del_all_imgsets(study_id):
    study = Study.query.filter_by(id=study_id).options(joinedload('imgsets')).first()
    error = None

    if request.method == "PUT":
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

    if request.method == "DELETE":
        for imgset in study.imgsets:
            db.session.delete(imgset)
        db.session.commit()

    #response
    response = {}
    imgsets = []
    for imgset in study.imgsets:
        imgsets.append(imgset.to_dict())
    response["imgsets"] = imgsets
    response["error"] = error
    return jsonify(response)



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
                            imgset_id=imgset.id,
                            scale_input=json.dumps(result_dict["scale_input"]))
            db.session.add(result)
            db.session.flush()
            picked_stack = Image_stack(result_id=result.id,
                                       div_id = result_dict["picked_stack"]["div_id"],
                                       name=result_dict["picked_stack"]["name"],
                                       viewport = json.dumps(result_dict["picked_stack"]["viewport"]))
            if any(result_dict["picked_stack"]["tool_state"]):
                picked_stack.tool_state = json.dumps(result_dict["picked_stack"]["tool_state"])
            db.session.add(picked_stack)
            for image_name in result_dict["picked_stack"]["image_names"]:
                image = [image for image in study.images if image.name == image_name]
                if image == []:
                    error = image_name + " not found part of study."
                else:
                    picked_stack.images.append(image[0])

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