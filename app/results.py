from flask import Blueprint, g, render_template, jsonify, request, url_for,make_response
from .auth import login_required, access_level_required
import json
import csv
import os
import re
from .DBmodel import Result, Study, User, db, EllipticalRoi,RectangleRoi,FreehandRoi, User_study_progress
from sqlalchemy import func
from sqlalchemy.orm import lazyload, joinedload
from itertools import chain
import io


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
                                                               lazyload('imgsets.image_stacks'),
                                                               lazyload('imgsets.results')).all()

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

# results save all
@bp.route('/results/<study_id>/<version>')
@login_required
@access_level_required([2])
def download_all(study_id,version):
    study = Study.query.filter_by(id=study_id).first()
    results = Result.query.filter_by(study_id=study_id).options(joinedload('imgset'),
                                                                joinedload('imgset.image_stacks'),
                                                                lazyload('imgset.results')).all()
    users = User.query.all()

    # write header
    file_name = study.title + '_all_results.csv'
    si = io.StringIO()
    writer = csv.writer(si, delimiter=';')
    header, max_numb_scale_measurments, max_numbtooldata_measurments, max_stack_size = write_header(study.design,results,version)
    writer.writerow(header)

    # write results
    for result in results:
        row = write_result_row(result,study.design,users,max_numb_scale_measurments, max_numbtooldata_measurments, max_stack_size,version)
        writer.writerow(row)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=" + file_name
    output.headers["Content-type"] = "text/csv"
    return output



def write_header(design,results,version):
    header = ["user","imgset"]
    # images shown
    for i in range(0, design.numb_refimg):
        header.append("ref_stack_" + str(i+1) + "_name")
        header.append("ref_stack_" + str(i+1) + "_files")
    for i in range(0, design.numb_img):
        header.append("stack_" + str(i+1) + "_name")
        header.append("stack_" + str(i+1) + "_files")



    # image picked etc
    header += ["picked_stack_name",
               "picked_stack_files",
               "date"]

    # get dimensions for table
    max_numb_scale_measurments = {}
    max_numbtooldata_measurments = {}
    max_stack_size = 0
    for result in results:
        # get max number scale measurements and annotations
        if result.scale_input != "null":
            # scale input is a list dictonaries
            # each scale is dict 
            # keys are the text 
            # values are two lists: scale values + uuid (needed to link to scale data)
            scale_input = json.loads(result.scale_input)
            for scale_text in scale_input.keys():
                if scale_text in max_numb_scale_measurments.keys():
                    max_numb_scale_measurments[scale_text] = max(max_numb_scale_measurments[scale_text], len(scale_input[scale_text]["values"]))
                else:
                    max_numb_scale_measurments[scale_text] = len(scale_input[scale_text]["values"])
        # get max numb for tool data columns (e.g. rois, length measurments)
        stack_picked = result.stack_picked
        max_stack_size = max(max_stack_size,len(stack_picked.images))
        if stack_picked.tool_state:
            # tools state is list of cornerstone tool states
            # each entry corresponds to an image within the stack
            # each tool state can consist of multiple roi and length measurments
            for i,image in enumerate(stack_picked.images):
                tool_state = json.loads(stack_picked.tool_state)[i]
                if tool_state:
                    for tool in tool_state:
                        if tool in max_numbtooldata_measurments.keys():
                            max_numbtooldata_measurments[tool] = max(max_numbtooldata_measurments[tool],len(tool_state[tool]["data"]))
                        else:
                            max_numbtooldata_measurments[tool] = len(tool_state[tool]["data"])

    # scale_input
    for scale_text in max_numb_scale_measurments.keys():
        for i in range(max_numb_scale_measurments[scale_text]):
            header.append(scale_text + "measurement " + str(i+1))

    # tools data columns
    for i in range(max_stack_size):
        for tool in max_numbtooldata_measurments.keys():
            for j in range(max_numbtooldata_measurments[tool]):
                header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_start")
                header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_end" )
                if "Roi" in tool:
                    header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_area")
                if "Length" in tool:
                    header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_length")
                
    # overlap columns
    for i in range(max_stack_size):
        for tool in max_numbtooldata_measurments.keys():
            for j in range(max_numbtooldata_measurments[tool]):
                if "Roi" in tool:
                    header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_ious")
                    header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_dice")
                    header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_perc")
    
    # add raw data columns
    if version=="full":
        for i in range(max_stack_size):
            for tool in max_numbtooldata_measurments.keys():
                for j in range(max_numbtooldata_measurments[tool]):
                    if "Roi" in tool:
                        header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_uuid")
                        header.append(scale_text + "_" + "_measurement_" + str(i+1) + "_uuid")
                        header.append("stackpos" + "_" + str(i+1) + "_" + tool + "_" + str(j+1) + "_raw_data")
        for i in range(0, design.numb_img):
            header.append("stack_" + str(i+1) + "_viewport_info")




    return header, max_numb_scale_measurments, max_numbtooldata_measurments, max_stack_size

def write_result_row(result,design,users, max_numb_scale_measurments, max_numbtooldata_measurments, max_stack_size, version):
    row = []
    # username and imgset pos
    user = [user.username for user in users if user.id ==
                result.user_id][0]
    row.append(user)
    imgset_position = result.imgset.position+1
    row.append(imgset_position)


    stack_picked = result.stack_picked
    # add stack infos
    ground_truth_tool_state = []
    range_images = chain(range(0, design.numb_refimg), range(2, design.numb_img+2))
    for i in range_images:
        div_id_ref = "dicom_img_" + str(i)
        stack = result.imgset.get_stack_by_div_id(div_id_ref)
        # stack can be none if left blank
        row.append(stack.name)
        row.append("|".join([image.name for image in stack.images]))
        # tools state and viewport only shown for none ref images
        if stack.name == stack_picked.name:
            ground_truth_tool_state = stack.tool_state


    # picked image and date
    row.append(stack_picked.name)
    row.append("|".join([image.name for image in stack_picked.images]))
    row.append(result.created)


    # scale input
    if result.scale_input and result.scale_input != "null":
        scale_input = json.loads(result.scale_input)
        row.extend(write_scale_input(scale_input,max_numb_scale_measurments))


    # tool measuremnts
    if stack_picked.tool_state:
        tool_data = write_tool_data(stack_picked.tool_state, max_numbtooldata_measurments, max_stack_size)
        row.extend(tool_data)

    # overlap metrics
    if ground_truth_tool_state and stack_picked.tool_state:        
        metrics = write_roi_metrics(stack_picked.tool_state, max_numbtooldata_measurments,max_stack_size, ground_truth_tool_state)
        row.extend(metrics)

    # raw data
    if version == "full":
        raw_data = write_raw_data(max_numb_scale_measurments, max_numbtooldata_measurments, max_stack_size)
        row.extend(raw_data)

    return row


def write_scale_input(scale_input, max_numb_scale_measurments):
    row = []
    # compatibility bug with old scale design (adjust db and remove these lines)
    if isinstance(scale_input,int):
        scale_input = {design.scales[0].text:{"values":[scale_input],"uuids":[]}}
    # loop over scale text in results because in an old version the results scale could differ from 
    # the design scale (changes to study after it already started)
    for scale_text in max_numb_scale_measurments.keys():
        if scale_text in scale_input.keys():
            scale_values = scale_input[scale_text]["values"]
            scale_uuids = scale_input[scale_text]["uuids"]

            # scales can have multiple values or just one depending on type
            # types: roi scales (repeated when roi drawn) and "normal"
            if len(scale_values)==max_numb_scale_measurments[scale_text]:
                row.extend(scale_values)
            else:
                row.extend(scale_values)
                for i in range(max_numb_scale_measurments[scale_text] - len(scale_values)):
                    row.append("")


    return row


def write_tool_data(stack_picked_tool_state,max_numbtooldata_measurments,max_stack_size):
    row = []    
    tool_state_images = json.loads(stack_picked_tool_state)

    # stack_picked_tool_state is list of cornerstone tool states
    # each entry corresponds to an image within the stack
    # each tool state can consist of multiple roi and length measurments    
    for i in range(max_stack_size):
        tool_state_image = tool_state_images[i]
        for tool in max_numbtooldata_measurments.keys():
            for j in range(max_numbtooldata_measurments[tool]):
                if tool in tool_state_image.keys() and len(tool_state_image[tool]["data"]) > j:
                    tool_state_image_data = tool_state_image[tool]["data"][j]
                    start_pos = (tool_state_image_data["handles"]["start"]["x"],
                                 tool_state_image_data["handles"]["start"]["y"])
                    end_pos = (tool_state_image_data["handles"]["end"]["x"],
                               tool_state_image_data["handles"]["end"]["y"])

                    row.append(start_pos)
                    row.append(end_pos)
                    # write area or length data
                    if "Roi" in tool:
                        row.append(str(round(tool_state_image_data["cachedStats"]["area"],2)))
                    if "Length" in tool:
                        row.append(str(round(tool_state_image[tool]["data"][j]["length"],2)))


                else:
                    row.extend(["","",""])


    return row

    

def write_roi_metrics(stack_picked_tool_state, max_numbtooldata_measurments, max_stack_size, ground_truth_tool_state):
    metrics = []
    tool_state_images = json.loads(stack_picked_tool_state)
    tool_state_images_gt = json.loads(ground_truth_tool_state)
    for i in range(max_stack_size):
        if len(tool_state_images) > i and len(tool_state_images_gt) > i:
            tool_state_image = tool_state_images[i]
            tool_state_image_gt = tool_state_images_gt[i]
        else:
            metrics.extend(["","",""])
            continue
        for tool in max_numbtooldata_measurments.keys():
            for j in range(max_numbtooldata_measurments[tool]):
                if tool in tool_state_image.keys() and len(tool_state_image[tool]["data"]) > j and \
                   tool in tool_state_image_gt.keys():
                    tool_data = {"data":[tool_state_image[tool]["data"][j]]}
                    roi = eval(tool + "(tool_data)" ) 
                    tool_data_gt = tool_state_image_gt[tool]
                    rois_gt = eval(tool + "(tool_data_gt)" )  
                    for metric in ["iou","dice","perc_correct_pixels"]:
                        metrics.append(max(rois_gt.calc_seq_metric(roi, metric)))
                else:
                    metrics.extend(["","",""])

    return metrics


def write_raw_data(max_numb_scale_measurments, max_numbtooldata_measurments, max_stack_size):
    raw_data = []
    return raw_data