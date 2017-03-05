from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from models import fetch_idsr
from models.idsr import Idsr

# Define the blueprint: 'idsrentry', set its url prefix: app.url/idsrentry
mod_idsrentry = Blueprint('idsrentry', __name__, url_prefix='/idsrentry')

@mod_idsrentry.route('/', methods=['GET', 'POST'])
@mod_idsrentry.route('/a')
@login_required
def stepA():
    """
    Renders the IDSR's form wizard at Step A - Basic information
    :returns: the html template for Step A
    """
    return _process_request('a')

@mod_idsrentry.route('/b')
@login_required
def stepB():
    """
    Renders the IDSR's form wizard at Step B - Diganosis information
    :returns: the html template for Step B
    """
    return _process_request('b')

@mod_idsrentry.route('/c')
@login_required
def stepC():
    """
    Renders the IDSR's form wizard at Step C - Patient Basic Information
    :returns: the html template for Step C
    """
    return _process_request('c')

@mod_idsrentry.route('/d')
@login_required
def stepD():
    """
    Renders the IDSR's form wizard at Step D - Clinical Information
    :returns: the html template for Step C
    """
    return _process_request('d')

def _process_request(step):
    """
    Renders the IDSR's form wizard at the step indicated.
    If a parameter 'id' is provided via get or post, the form is displayed with
    the input fields filled with previously submitted data that corresponds to
    the given id, but only if the logged user has enough privileges (the user
    is the creator and/or with admin role). Otherwise, redirects to an error
    page stating the user has not enough privileges.
    If an 'id' is provided and the conditions explained above are met but the
    form was already transferred to Bika, then all fields will be filled, but
    in readonly mode.

    :param step: the step to load
    :param type: string
    :returns: the html template for Step B
    """
    id = request.args.get('id')
    if id:
        idsrform = fetch_idsr(id)
        if idsrform:
            #TODO Check the user has enough privileges if previously data is available
            idsr = idsrform
        else:
            flash("No IDSR Form found")
            urlid = 'idsrentry.step%s' % step.upper()
            return redirect(url_for(urlid))
    urltemplate = 'idsrentry/step_%s/index.html' % step
    return render_template(urltemplate)
