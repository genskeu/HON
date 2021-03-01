from flask import (
    Blueprint, flash, redirect, render_template, request, url_for,
    jsonify, current_app, g, session
)
from .auth import login_required, access_level_required
from .DBmodel import RectangleRoi,EllipticalRoi


bp = Blueprint("misc", __name__)

#test calc of overlap
@bp.route('/overlap', methods=['POST'])
@login_required
@access_level_required([2])
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
@login_required
@access_level_required([2,3])
def tutorials():
    return render_template("tutorials/overview.html")