import os
from flask import request, current_app, send_file, redirect, Blueprint,abort, jsonify, g
from werkzeug.utils import secure_filename
import zipfile
from .DBmodel import Study, Image, db
from .auth import login_required, access_level_required


# return files on request
bp = Blueprint("file_handeling", __name__)
@bp.route("/get_file/<int:user_id>/<int:study_id>/<image_name>",methods=['GET'])
@login_required
@access_level_required([1,2])
def get_file(user_id,study_id,image_name):
    file_path = os.path.join(current_app.config['IMAGE_PATH'],str(user_id),str(study_id),image_name)
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        abort(404, description="Resource not found")

# upload images
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'dcm', 'zip', 'png'])


def allowed_file(filename):
    file_type=filename.split('.')[-1]
    return '.' in filename and \
           file_type.lower() in ALLOWED_EXTENSIONS


# code from flask-tutorial
def upload_files(files, study_dir):
    for file in files.getlist('file'):
        # if user does not select file, browser also
        # submit an empty part without filename
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(study_dir, filename))
            if "zip" == filename[-3:]:
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(study_dir)
                    zip_ref.close
                    os.remove(os.path.join(study_dir, filename))



# add files to study
@bp.route('/add_files/<int:study_id>', methods=['POST'])
@login_required
@access_level_required([2])
def add_files(study_id):
    study = Study.query.filter_by(id=study_id).first()
    image_dir = study.get_image_dir()
    files = request.files
    filenames = []
    for f in files.getlist('file'):
        filename = secure_filename(f.filename)
        filenames.append(f.filename)
        if filename not in [image.name for image in study.images] and allowed_file(filename):
            image = Image(name=filename,base_url=request.url_root + "get_file/{}/{}/".format(g.user.id,study.id))
            study.images.append(image)
    upload_files(files, image_dir)
    db.session.commit()

    # validate that db entries == files in image dir and get names of files exisitng in both
    response = {}
    image_names,image_names_err = validate_imagedir_imagedb(study)
    image_names_added = [image_name for image_name in image_names if image_name in filenames]
    response["image_names"] = image_names
    response["image_names_err"] = image_names_err
    response["image_names_added"] = image_names_added
    return jsonify(response)


# get filenames of files attached to a study
@bp.route('/get_filenames/<int:study_id>', methods=['GET'])
@login_required
@access_level_required([2])
def get_filenames(study_id):
    study = Study.query.filter_by(id=study_id).first()
    response = {}    
   
    # validate that db entries == files in image dir and get names of files exisitng in both
    image_names = validate_imagedir_imagedb(study)[0]
    response["image_names"] = image_names

    return jsonify(response)


# delete files
@bp.route('/delete_files/<int:study_id>', methods=['DELETE'])
@login_required
@access_level_required([2])
def delete_files(study_id):
    response = {}     
    study = Study.query.filter_by(id=study_id).first()
    image_dir = study.get_image_dir()   
    filenames = request.get_json()
    for f in filenames:
        image_path = os.path.join(image_dir,f)
        os.remove(image_path)
        base_url=request.url_root + "get_file/{}/{}/".format(g.user.id,study.id)
        image = Image.query.filter_by(name = f,base_url=base_url).first()
        db.session.delete(image)
        db.session.commit()

    # validate that db entries == files in image dir and get names of files exisitng in both
    image_names = validate_imagedir_imagedb(study)[0]
    response["image_names"] = image_names
    return jsonify(response)


# check db entries and files in image dir are identical
def validate_imagedir_imagedb(study):
    image_dir = study.get_image_dir()
    image_names_db = set([image.name for image in study.images])
    image_names_dir = set(os.listdir(image_dir))

    image_names = image_names_db.intersection(image_names_dir)
    image_names_db_only = image_names_db.difference(image_names_dir)
    image_names_dir_only = image_names_dir.difference(image_names_db)
    for image_name_db_only in image_names_db_only:
        base_url=request.url_root + "get_file/{}/{}/".format(g.user.id,study.id)
        image = Image.query.filter_by(name = image_name_db_only,base_url=base_url).first()
        db.session.delete(image)
    db.session.commit()
    
    for image_name_dir_only in image_names_dir_only:
        image_path = os.path.join(image_dir,image_name_dir_only)
        os.remove(image_path)

    return list(image_names), list(image_names_db_only) + list(image_names_dir_only)