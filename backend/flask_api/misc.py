from flask import Blueprint, flash, render_template, request, jsonify
from .auth import access_level_required
from .DBmodel import RectangleRoi,EllipticalRoi
from flask_jwt_extended import jwt_required


bp = Blueprint("misc", __name__)

#test calc of overlap
@bp.route('/overlap', methods=['POST'])
@jwt_required()
@access_level_required(["study_admin"])
def overlap():
    error = None
    if request.method == "POST":
        image = request.get_json()
        ellipses = EllipticalRoi((image["tool_state"]["EllipticalRoi"]))
        ellipses_gt = EllipticalRoi((image["tool_state"]["EllipticalRoi"]))
        return jsonify(ellipses.calc_ious(ellipses_gt))
    flash(error)


#test calc of overlap
@bp.route('/tutorials', methods=['GET'])
@jwt_required()
@access_level_required([2,3])
def tutorials():
    return render_template("tutorials/overview.html")