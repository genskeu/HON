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
    writer.writerow(get_header(study.design,version))

    # write results
    for result in results:
        row = get_result_row(result,study.design,users,version)
        writer.writerow(row)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=" + file_name
    output.headers["Content-type"] = "text/csv"
    return output

def get_header(design,version):
    header = ["user","imgset"]
    # images shown
    for i in range(0, design.numb_refimg):
        header.append("ref_stack_" + str(i+1) + "_name")
        header.append("ref_stack_" + str(i+1) + "_files")
    for i in range(0, design.numb_img):
        header.append("stack_" + str(i+1) + "_name")
        header.append("stack_" + str(i+1) + "_files")
        if version == "full":
            header.append("stack_" + str(i+1) + "_tool_states")
            header.append("stack_" + str(i+1) + "_viewport_info")

    # scale_input
    for i in range(len(design.scales)):
        header.append("scale_text_" + str(i+1)  )
        header.append("scale_values_" + str(i+1))
        if version == "full":
            header.append("scale_values_uuids_" + str(i+1))

    # image picked etc
    header += ["picked_stack_name",
               "picked_stack_files",
               "picked_stack_tool_states",
               "date",
               "length_measurements",
               "length_start",
               "length_end",
               "perc_correct_pixels",
               "ious", 
               "dice"]

    if version == "short":
        header.remove("picked_stack_tool_states")

    return header

def get_result_row(result,design,users,version):
    row = []
    # username and imgset pos
    user = [user.username for user in users if user.id ==
                result.user_id][0]
    row.append(user)
    imgset_position = result.imgset.position+1
    row.append(imgset_position)


    stack_picked = result.stack_picked
    # add stack infos
    tool_state_gt = []
    range_images = chain(range(0, design.numb_refimg), range(2, design.numb_img+2))
    for i in range_images:
        div_id_ref = "dicom_img_" + str(i)
        stack = result.imgset.get_stack_by_div_id(div_id_ref)
        # stack can be none if left blank
        if stack:
            row.append(stack.name)
            row.append("|".join([image.name for image in stack.images]))
            # tools state and viewport only shown for none ref images
            if i > 1 and version == "full":
                row.append(stack.tool_state)
                row.append(stack.viewport)
            if stack.name == stack_picked.name:
                tool_state_gt = stack.tool_state
        else:
            if i > 1 and version == "full":
                row.append([None, None, None, None])
            else:
                row.append([None, None])

    # scale input
    if result.scale_input:
        scale_input = json.loads(result.scale_input)
        # compatibility bug with old scale design (adjust db and remove these lines)
        if isinstance(scale_input,int):
            scale_input = {design.scales[0].text:{"values":[scale_input],"uuids":[]}}
    for i in range(len(design.scales)):
        row.append(design.scales[i].text)
        scale_values = scale_input[design.scales[i].text]["values"]
        # scales can have multiple values or just one depending on type
        # types: roi scales (repeated when roi drawn) and "normal"
        if len(scale_values):
            row.append(scale_values[0])
        else:
            row.append("")
        if version == "full":
            row.append(scale_input[design.scales[i].text]["uuids"])


    # picked image etc.
    row.append(stack_picked.name)
    row.append("|".join([image.name for image in stack_picked.images]))
    if version == "full":
        row.append(stack_picked.tool_state)
    row.append(result.created)


    # length measuremnts
    length_info = ""
    length_start = ""
    length_end = ""

    if stack_picked.tool_state:
        if "Length" in stack_picked.tool_state:
            for i in range(len([image.name for image in stack_picked.images])):
                tool_state = json.loads(stack_picked.tool_state)[i]
                length = []
                start = []
                end = []
                if tool_state:
                    length_data_raw = json.loads(stack_picked.tool_state)[i]["Length"]["data"]
                    length = [str(round(length_raw["length"],2)) for length_raw in length_data_raw]
                    start = ["x:" + str(round(length_raw["handles"]["start"]["x"],2)) + " y:" + str(round(length_raw["handles"]["start"]["y"],2)) for length_raw in length_data_raw]
                    end = ["x:" + str(round(length_raw["handles"]["end"]["x"],2)) + " y:" + str(round(length_raw["handles"]["end"]["y"],2)) for length_raw in length_data_raw]
                if i > 0:
                    length_info += "|"
                    length_start += "|"
                    length_end += "|"

                length_info += " / ".join(length)
                length_start += " / ".join(start)
                length_end += " / ".join(end)

    row.append(length_info)
    row.append(length_start)
    row.append(length_end)
    
    row += calc_roi_metric(stack_picked,tool_state_gt,"perc_correct_pixels")
    row += calc_roi_metric(stack_picked,tool_state_gt,"iou")
    row += calc_roi_metric(stack_picked,tool_state_gt,"dice")

    return row


def calc_roi_metric(stack_picked,tool_state_gt,metric):
    #calc ious and perc correct for all roi tools
    cell = []
    for i in range(len([stack_picked.images])):
        results = []
        if tool_state_gt and stack_picked.tool_state:
            tool_state_image_gt = json.loads(tool_state_gt)[i]
            tool_state_image_pi = json.loads(stack_picked.tool_state)[i]
        else:
            continue
        # filter and only keep valid tool data (rois)
        roi_types = ["EllipticalRoi", "RectangleRoi", "FreehandRoi"]
        tool_state_image_gt_filtered = {}
        tool_state_image_pi_filtered = {}
        for roi_type in roi_types:
            if roi_type in tool_state_image_gt.keys():
                tool_state_image_gt_filtered[roi_type] = tool_state_image_gt[roi_type]
            if roi_type in tool_state_image_pi.keys():
                tool_state_image_pi_filtered[roi_type] = tool_state_image_pi[roi_type]
        # calc metrics
        for roi_type_gt in tool_state_image_gt_filtered.keys():
            for roi_type_pi in tool_state_image_pi_filtered.keys():            
                Roi_gt = eval(roi_type_gt + "(tool_state_image_gt_filtered" + "['" + roi_type_gt + "'])" )  
                Roi_pi = eval(roi_type_pi + "(tool_state_image_pi_filtered" + "['" + roi_type_pi + "'])" ) 
                calc_metrics = Roi_pi.calc_seq_metric(Roi_gt, metric)
                calc_metrics = [str(calc_metric) for calc_metric in calc_metrics]
                results += calc_metrics
        cell.append(" ".join(results))
    cell = [" | ".join(cell)]
    return cell


"""    if stack_picked.tool_state and tool_state_gt:
        roi_types = ["EllipticalRoi", "RectangleRoi", "FreehandRoi"]
        for roi_type in roi_types:
            if roi_type in tool_state_gt and roi_type in stack_picked.tool_state:"""