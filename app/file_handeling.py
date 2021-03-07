import os
from flask import flash, request, current_app, send_file, redirect, Blueprint,abort, jsonify, g
from werkzeug.utils import secure_filename
import zipfile
from .DBmodel import Study, Image, db
from .auth import login_required, access_level_required


# return dicoms on request
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
    # check if the post request has the file part
    if 'file' not in files:
        flash('No files selected')
        return redirect(request.url)
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



#retrieve , upload or delete files to study API endpoint returning json
@bp.route('/files/<int:study_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
@access_level_required([2])
def files(study_id):
    study = Study.query.filter_by(id=study_id).first()
    image_dir = study.get_image_dir()
    image_names = [image.name for image in study.images]
    response = {}

    if request.method == "POST":
        files = request.files
        for f in files.getlist('file'):
            filename = secure_filename(f.filename)
            if filename not in [image.name for image in study.images] and allowed_file(filename):
                image = Image(name=filename,base_url=request.url_root + "get_file/{}/{}/".format(g.user.id,study.id))
                study.images.append(image)
        upload_files(files, image_dir)
        db.session.commit()
        image_names = os.listdir(image_dir)
        response["image_names"] = image_names
        response["file_names"] = ""
        for file in files.getlist('file'):
            # if user does not select file, browser also
            # submit an empty part without filename
            response["file_names"] += file.filename
        return jsonify(response)

    if request.method == "DELETE":
        file_names = request.get_json()
        for f in file_names:
            image_path = os.path.join(image_dir,f)
            os.remove(image_path)
            base_url=request.url_root + "get_file/{}/{}/".format(g.user.id,study.id)
            image = Image.query.filter_by(name = f,base_url = base_url).first()
            db.session.delete(image)
            db.session.commit()
        image_names = os.listdir(image_dir)

    response["image_names"] = image_names
    return jsonify(response)
