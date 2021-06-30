from app.studies import study
from flask import Blueprint, g, render_template, jsonify, request, url_for,make_response, current_app
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
import ast

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
@bp.route('/results/<study_id>',methods=["POST"])
@login_required
@access_level_required([2])
def download_all(study_id):
    study = Study.query.filter_by(id=study_id).first()
    results = Result.query.filter_by(study_id=study_id).options(joinedload('imgset'),
                                                                joinedload('imgset.image_stacks'),
                                                                lazyload('imgset.results')).all()
    users = User.query.all()
    version = "short"
    if request.form.get("include_raw_data"):
        version = "full"

    # write header
    file_name = study.title + '_all_results.csv'
    si = io.StringIO()
    writer = csv.writer(si, delimiter=';')
    header, max_numb_scale_measurments, max_numbtooldata_measurments_sp, max_stack_size_sp, max_numbtooldata_measurments_gt, max_stack_size_gt = write_header(study.design,results,study.imgsets,version)
    writer.writerow(header)

    # write column explanation (optional)
    if request.form.get("include_explanations"):
        expl = get_expl(header,max_numb_scale_measurments,max_numbtooldata_measurments_sp)
        writer.writerow(expl)

    # write results
    for result in results:
        row = write_result_row(result,study.design,users,max_numb_scale_measurments, max_numbtooldata_measurments_sp, max_stack_size_sp, max_numbtooldata_measurments_gt, max_stack_size_gt,version)
        writer.writerow(row)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=" + file_name
    output.headers["Content-type"] = "text/csv"

    return output



def write_header(design,results,imgsets,version):
    header = ["user","imageset-id"]

    # get dimensions for table
    max_numb_scale_measurments = {}
    max_numbtooldata_measurments_sp = {}
    max_stack_size_sp = 0
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
        max_stack_size_sp = max(max_stack_size_sp,len(stack_picked.images))
        if stack_picked.tool_state:
            # tools state is list of cornerstone tool states
            # each entry corresponds to an image within the stack
            # each tool state can consist of multiple roi and length measurments
            for i,image in enumerate(stack_picked.images):
                tool_state = json.loads(stack_picked.tool_state)[i]
                if tool_state:
                    for tool in tool_state:
                        if tool in max_numbtooldata_measurments_sp.keys():
                            max_numbtooldata_measurments_sp[tool] = max(max_numbtooldata_measurments_sp[tool],len(tool_state[tool]["data"]))
                        else:
                            max_numbtooldata_measurments_sp[tool] = len(tool_state[tool]["data"])
    
    max_numbtooldata_measurments_gt = {}
    max_stack_size_gt = 0
    for imageset in imgsets:
        for stack in imageset.image_stacks:
            max_stack_size_gt = max(max_stack_size_gt,len(stack.images))
            if stack.tool_state:
            # tools state is list of cornerstone tool states
            # each entry corresponds to an image within the stack
            # each tool state can consist of multiple roi and length measurments
                for i,image in enumerate(stack.images):
                    tool_state = json.loads(stack.tool_state)[i]
                    if tool_state:
                        for tool in tool_state:
                            if tool in max_numbtooldata_measurments_gt.keys():
                                max_numbtooldata_measurments_gt[tool] = max(max_numbtooldata_measurments_gt[tool],len(tool_state[tool]["data"]))
                            else:
                                max_numbtooldata_measurments_gt[tool] = len(tool_state[tool]["data"])
    
    
    # images shown
    for i in range(0, design.numb_refimg):
        if max_stack_size_sp>1:
            header.append("stack-name-ref-iv" + str(i+1))
        header.append("filename(s)-ref-iv" + str(i+1))
    for i in range(0, design.numb_img):
        if max_stack_size_sp>1:
            header.append("stack-name-iv" + str(i+1))
        header.append("filename(s)-iv" + str(i+1))


    # image picked etc
    if design.numb_img > 1:
        if max_stack_size_sp>1:
            header += ["stack-name-sp"]
        header += ["filename(s)-sp"]


    header += ["date"]

    # scale_input
    for scale_text in max_numb_scale_measurments.keys():
        for i in range(max_numb_scale_measurments[scale_text]):
            header.append(scale_text + " measurement " + str(i+1))

    # tools data columns
    for i in range(max_stack_size_sp):
        for tool in max_numbtooldata_measurments_sp.keys():
            for j in range(max_numbtooldata_measurments_sp[tool]):
                header.append("sp-" + tool + str(j+1) + "-start-stackpos" + str(i+1))
                header.append("sp-" + tool + str(j+1) + "-end-stackpos" + str(i+1) )
                if "Roi" in tool:
                    header.append("sp-" + tool + str(j+1) + "-area-stackpos" + str(i+1))
                if "Length" in tool:
                    header.append("sp-" + tool + str(j+1) + "-length-stackpos" + str(i+1))


    for i in range(max_stack_size_gt):
        for tool in max_numbtooldata_measurments_gt.keys():
            for j in range(max_numbtooldata_measurments_gt[tool]):
                header.append("gt-" + tool + str(j+1) + "-start-stackpos" + str(i+1))
                header.append("gt-" + tool + str(j+1) + "-end-stackpos" + str(i+1) )
                if "Roi" in tool:
                    header.append("gt-" + tool + str(j+1) + "-area-stackpos" + str(i+1))
                if "Length" in tool:
                    header.append("gt-" + tool + str(j+1) + "-length-stackpos" + str(i+1))
                
    # overlap columns
    for i in range(max_stack_size_gt):
        for tool in max_numbtooldata_measurments_gt.keys():
            for j in range(max_numbtooldata_measurments_gt[tool]):
                if "Roi" in tool:
                    header.append(tool + str(j+1) + "-iou-stackpos" + str(i+1))
                    header.append(tool + str(j+1) + "-dice-stackpos" + str(i+1))
                    header.append(tool + str(j+1) + "-perc-stackpos" + str(i+1))
    
    # add raw data columns
    if version=="full":
        for i in range(max_stack_size_sp):
            for tool in max_numbtooldata_measurments_sp.keys():
                for j in range(max_numbtooldata_measurments_sp[tool]):
                    header.append("sp-rawdata-" + tool + str(j+1) + "stackpos-" + str(i+1))

        for i in range(max_stack_size_gt):
            for tool in max_numbtooldata_measurments_gt.keys():
                for j in range(max_numbtooldata_measurments_gt[tool]):
                    header.append("gt-rawdata-" + tool + str(j+1) + "stackpos-" + str(i+1))

        header.append("rawdata-imageviewer-study-participant-selection")




    return header, max_numb_scale_measurments, max_numbtooldata_measurments_sp, max_stack_size_sp, max_numbtooldata_measurments_gt, max_stack_size_gt

def write_result_row(result,design,users, max_numb_scale_measurments, max_numbtooldata_measurments_sp, max_stack_size_sp, max_numbtooldata_measurments_gt, max_stack_size_gt, version):
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
        if max_stack_size_sp>1:
            row.append(stack.name)
        row.append("|".join([image.name for image in stack.images]))
        # tools state and viewport only shown for none ref images
        if stack.name == stack_picked.name:
            ground_truth_tool_state = stack.tool_state


    # picked image and date
    if max_stack_size_sp>1:
        row.append(stack_picked.name)
    if len(stack_picked.images) > 1:
        row.append("|".join([image.name for image in stack_picked.images]))
    row.append(result.created)


    # scale input
    if result.scale_input and result.scale_input != "null":
        scale_input = json.loads(result.scale_input)
        row.extend(write_scale_input(scale_input,max_numb_scale_measurments))


    # tool measuremnts
    if stack_picked.tool_state:
        tool_data = write_tool_data(stack_picked.tool_state, max_numbtooldata_measurments_sp, max_stack_size_sp, ground_truth_tool_state, max_numbtooldata_measurments_gt, max_stack_size_gt)
        row.extend(tool_data)
    else:
        for i in range(max_stack_size_sp):
            for tool in max_numbtooldata_measurments_sp.keys():
                for j in range(max_numbtooldata_measurments_sp[tool]):
                    row.extend(["","",""])
        for i in range(max_stack_size_gt):
            for tool in max_numbtooldata_measurments_gt.keys():
                for j in range(max_numbtooldata_measurments_gt[tool]):
                    row.extend(["","",""])

    # overlap metrics
    if ground_truth_tool_state and stack_picked.tool_state:        
        metrics = write_roi_metrics(stack_picked.tool_state, max_numbtooldata_measurments_gt, max_stack_size_gt, ground_truth_tool_state)
        row.extend(metrics)
    else:
        for i in range(max_stack_size_gt):
            for tool in max_numbtooldata_measurments_gt.keys():
                for j in range(max_numbtooldata_measurments_gt[tool]):
                    row.extend(["","",""])

    # raw data
    if version == "full":
        raw_data = write_raw_data(ground_truth_tool_state, stack_picked.tool_state, stack.viewport)
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


def write_tool_data(stack_picked_tool_state,max_numbtooldata_measurments_sp, max_stack_size_sp, ground_truth_tool_state, max_numbtooldata_measurments_gt, max_stack_size_gt):
    row = []    
    tool_state_images = json.loads(stack_picked_tool_state)

    # stack_picked_tool_state is list of cornerstone tool states
    # each entry corresponds to an image within the stack
    # each tool state can consist of multiple roi and length measurments    
    for i in range(max_stack_size_sp):
        tool_state_image = tool_state_images[i]
        for tool in max_numbtooldata_measurments_sp.keys():
            for j in range(max_numbtooldata_measurments_sp[tool]):
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

    tool_state_images = json.loads(ground_truth_tool_state)
 
    for i in range(max_stack_size_gt):
        tool_state_image = tool_state_images[i]
        for tool in max_numbtooldata_measurments_gt.keys():
            for j in range(max_numbtooldata_measurments_gt[tool]):
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


def write_raw_data(ground_truth_tool_state, sp_tool_state, sp_viewport):
    raw_data = []
    if ground_truth_tool_state:
        raw_data.append(ground_truth_tool_state)
    if sp_tool_state:
        raw_data.append(sp_tool_state)
    if sp_viewport:
        raw_data.append(sp_viewport)
    return raw_data


def get_expl(header,max_numb_scale_measurments,max_numbtooldata_measurments_sp):
    expl = []
    file = open(os.path.join(current_app.static_folder,"column_explanations.txt"), "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    for heading in header:
        repeat_heading = re.sub('\d','*',heading)
        scale_heading = re.sub(" measurement 1","",heading)
        # image names etc
        if heading in dictionary.keys():
            expl.append(dictionary[heading])
        elif repeat_heading in dictionary.keys():
            expl.append(dictionary[repeat_heading])
        # scale explanations
        elif scale_heading in max_numb_scale_measurments.keys():
            expl.append(dictionary["scale1"])
        elif "measurement" in heading:
            expl.append(dictionary["scale*"])
        # ann explanations
        elif max_numbtooldata_measurments_sp:
            for tool in max_numbtooldata_measurments_sp.keys():
                ann_heading = re.sub(tool,"ann",heading)
                if ann_heading in dictionary.keys() and tool in heading:
                    print(ann_heading)
                    expl.append(dictionary[ann_heading])
        else:
            expl.append("")

    print(max_numb_scale_measurments.keys())
    return expl