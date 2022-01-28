import os
from flask import request, current_app, send_file, Blueprint,abort, jsonify, g
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


# helper functions fpr file upload
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'dcm', 'zip', 'png'])


def allowed_file(filename):
    file_type=filename.split('.')[-1]
    return '.' in filename and \
           file_type.lower() in ALLOWED_EXTENSIONS

# upload files to study
@bp.route('/upload_files/<int:study_id>', methods=['POST'])
@login_required
@access_level_required([2])
def upload_files(study_id):
    study = Study.query.filter_by(id=study_id).first()
    image_dir = study.get_image_dir()
    image_names_study = [image.name for image in study.images]
    files = request.files
    filenames_saved = []
    filenames_not_saved = []
    
    # save file to image dir
    for f in files.getlist('file'):
        filename = secure_filename(f.filename)
        if filename not in image_names_study and allowed_file(filename):
            try:
                f.save(os.path.join(image_dir, filename))
            except:
                print("Error saving {}.".format(filename))
            else:
                filenames_saved.append(f.filename)
            if "zip" == filename[-3:]:
                filenames_saved.remove(f.filename)
                filenames_unzipped, filenames_not_unzipped = unzip_images(filename, image_dir, study)
                filenames_saved += filenames_unzipped
                filenames_not_saved += filenames_not_unzipped
        else:
            filenames_not_saved.append(filename)

    # save image infos to db
    for filename in filenames_saved:
        image = Image(name=filename,base_url=request.url_root + "get_file/{}/{}/".format(g.user.id,study.id))
        try:
            study.images.append(image)
        except:
            print("Error saving image {} to database for study {} {}.".format(filename,study.title, study.id))
            os.remove(os.path.join(image_dir, filename))
            filenames_saved.remove(filename)
            filenames_not_saved.append(filename)            
    db.session.commit()

    response = {}
    response["filenames_db"] = [image.name for image in study.images]
    response["filenames_not_saved"] = filenames_not_saved
    response["filenames_saved"] = filenames_saved
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
@login_required
@access_level_required([2])
def get_filenames(study_id):
    study = Study.query.filter_by(id=study_id).first()
    response = {}    
   
    image_names_db = [image.name for image in study.images]
    response["filenames_db"] = image_names_db

    return jsonify(response)


# delete files
@bp.route('/delete_files/<int:study_id>', methods=['DELETE'])
@login_required
@access_level_required([2])
def delete_files(study_id):
    study = Study.query.filter_by(id=study_id).first()
    image_dir = study.get_image_dir()   
    filenames = request.get_json()
    files_del = []
    files_not_del = []

    # delete from db
    for filename in filenames:
        base_url=request.url_root + "get_file/{}/{}/".format(g.user.id,study.id)
        image = Image.query.filter_by(name = filename,base_url=base_url).first()
        try:
            db.session.delete(image)
        except:
            print("Error deleting image {} from database for study {} {}.".format(filename, study.title, study.id))
            files_not_del.append(filename)
        else:
            files_del.append(filename)
    db.session.commit()

    # delete from dir
    image_names_dir = os.listdir(image_dir)
    for filename in filenames:
        if filename in image_names_dir:    
            try:
                image_path = os.path.join(image_dir,filename)
                os.remove(image_path)
            except:
                print("Error deleting image {} from dir for study {} {}.".format(image_path,study.title, study.id))
    
    response = {}     
    image_names_db = [image.name for image in study.images]
    response["filenames_db"] = image_names_db
    response["files_del"] = files_del
    response["files_not_del"] = files_not_del
    return jsonify(response)


