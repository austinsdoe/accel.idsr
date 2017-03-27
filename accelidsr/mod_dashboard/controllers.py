from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from accelidsr.mod_idsrentry.models.idsr import Idsr
from accelidsr.mod_idsrentry.models import find_all

# Define the blueprint: 'auth', set its url prefix: app.url/dashboard
mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@mod_dashboard.route('/idsrlist')
@login_required
def idsrlist():
    """
    Displays a view that contains a list with the IDSR Forms that have been
    created, together with information regarding their current status, the
    name of the user that created each one, etc. Also displays some filtering
    buttons, as well as other actions for the creation, edition, etc. of IDSRs
    """
    items = Idsr.findAll()
    urltemplate = 'dashboard/index.html'
    return render_template(urltemplate, items=items)
