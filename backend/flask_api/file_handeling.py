import os
from flask import request, current_app, send_file, Blueprint,abort, jsonify, g
from werkzeug.utils import secure_filename
import zipfile
from .DBmodel import Study, Image, db
from .auth import access_level_required
from flask_jwt_extended import jwt_required, get_jwt_identity
import shutil


# return files on request
bp = Blueprint("file_handeling", __name__)
@bp.route("/get_file/<int:user_id>/<int:study_id>/<stack_name>/<image_name>",methods=['GET'])
#@jwt_required()
#@access_level_required([1,2])
def get_file(user_id,study_id,stack_name,image_name):
    file_path = os.path.join(current_app.config['IMAGE_PATH'],str(user_id),str(study_id),stack_name,image_name)
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        abort(404, description="Resource not found")


# helper functions fpr file upload
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'dcm', 'zip', 'png'])


def allowed_file(filename):
    file_type=filename.split('.')[-1]
    return '.' in filename and \
           file_type.lower() in ALLOWED_EXTENSIONS

# upload files to study
@bp.route('/upload_files/<int:study_id>', methods=['POST'])
@jwt_required()
def upload_files(study_id):
    study = Study.query.filter_by(id=study_id).first()
    user_id = get_jwt_identity()
    image_dir = study.get_image_dir()
    image_urls_study = [image.base_url + image.name for image in study.images]
    files = request.files
    filenames_saved = []
    filenames_not_saved = []
    
    # save file to image dir
    for f in files.getlist('file'):
        path = os.path.normpath(f.filename).split(os.sep)
        if len(path) > 1:
            folder, filename = path[-2], path[-1]
        else:
            folder, filename = path[-1].split(".")[0], path[-1]
        filename = secure_filename(filename)
        folder = secure_filename(folder)
        base_url = request.url_root + f"get_file/{user_id}/{study.id}/{folder}/"
        if base_url + filename not in image_urls_study and allowed_file(filename):
            stack_dir = os.path.join(image_dir, folder)
            if not os.path.isdir(stack_dir):
                os.mkdir(os.path.join(image_dir, folder))
            try:
                f.save(os.path.join(stack_dir, filename))
            except:
                print("Error saving {}.".format(filename))
            else:
                filenames_saved.append(filename)
            # not working
            # if "zip" == filename[-3:]:
            #     filenames_saved.remove(f.filename)
            #     filenames_unzipped, filenames_not_unzipped = unzip_images(filename, image_dir, study)
            #     filenames_saved += filenames_unzipped
            #     filenames_not_saved += filenames_not_unzipped
        else:
            filenames_not_saved.append(filename)

    # save image infos to db
    for filename in filenames_saved:
        image = Image(name=filename,base_url=base_url)
        try:
            study.images.append(image)
        except:
            print("Error saving image {} to database for study {} {}.".format(filename,study.title, study.id))
            os.remove(os.path.join(image_dir, filename))
            filenames_saved.remove(filename)
            filenames_not_saved.append(filename)            
    db.session.commit()

    stack = study.get_stack(stack_dir)
    response = {}
    response["filenames_db"] = [image.name for image in study.images]
    response["filenames_not_saved"] = filenames_not_saved
    response["filenames_saved"] = filenames_saved
    response["stack"] = stack
    return jsonify(response)


# unzip fct
def unzip_images(image_zip,image_dir, study):
    with zipfile.ZipFile(os.path.join(image_dir, image_zip), 'r') as zip_ref:
        zip_infolist = zip_ref.infolist()
        filenames_unzipped = []
        filenames_not_unzipped = []
        for zip_info in zip_infolist:
            # skip directories
            filename = os.path.basename(zip_info.filename)
            if filename not in [image.name for image in study.images] and allowed_file(filename):
                try:
                    zip_info.filename = filename
                    zip_ref.extract(zip_info, image_dir)
                except:
                    print("Error unzipping {}.".format(filename))
                else:
                    filenames_unzipped.append(filename)
            else:
                filenames_not_unzipped.append(filename)
    zip_ref.close
    try:
        os.remove(os.path.join(image_dir, image_zip)) 
    except:
        print("Error removing {}.".format(image_zip))

    return filenames_unzipped, filenames_not_unzipped



# get filenames of files attached to a study
@bp.route('/get_filenames/<int:study_id>', methods=['GET'])
@jwt_required()
@access_level_required(["study_admin"])
def get_filenames(study_id):
    study = Study.query.filter_by(id=study_id).first()
    response = {}    
   
    image_names_db = [image.name for image in study.images]
    response["filenames_db"] = image_names_db

    return jsonify(response)


# delete files
@bp.route('/delete_files/<int:study_id>', methods=['DELETE'])
@jwt_required()
@access_level_required(["study_admin"])
def delete_files(study_id):
    study = Study.query.filter_by(id=study_id).first()
    image_dir = study.get_image_dir()
    user_id = get_jwt_identity()
    stacks = request.get_json()
    stacks_del = []
    stacks_not_del = []

    # delete from db
    for stack in stacks:
        base_url = request.url_root + f"get_file/{user_id}/{study.id}/{stack['name']}/"
        for filename in stack["files"]:
            image = Image.query.filter_by(name = filename, base_url=base_url).first()
            try:
                db.session.delete(image)
            except:
                print(f"Error deleting image {filename} from database for study {study.title} {study.id}.")
                stacks_not_del.append(filename)
            else:
                stacks_del.append(filename)
        db.session.commit()

        # delete from dir
        image_names_dir = os.listdir(os.path.join(image_dir,stack["name"]))
        for filename in stack["files"]:
            if filename in image_names_dir:    
                try:
                    image_path = os.path.join(image_dir,stack["name"],filename)
                    os.remove(image_path)
                except:
                    print("Error deleting image {} from dir for study {} {}.".format(image_path,study.title, study.id))

        if len(os.listdir(os.path.join(image_dir,stack["name"]))) == 0:
            shutil.rmtree(os.path.join(image_dir,stack["name"]))
    
    response = {}     
    image_names_db = [image.name for image in study.images]
    response["filenames_db"] = image_names_db
    response["files_del"] = stacks_del
    response["files_not_del"] = stacks_not_del
    return jsonify(response)


