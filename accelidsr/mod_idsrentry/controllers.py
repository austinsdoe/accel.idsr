from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from models import fetch_idsr
from models.idsr import Idsr
from accelidsr.mod_idsrentry.forms import getAvailableSteps
from accelidsr.mod_idsrentry.forms import newIdsrEntryForm

# Define the blueprint: 'idsrentry', set its url prefix: app.url/idsrentry
mod_idsrentry = Blueprint('idsrentry', __name__, url_prefix='/idsrentry')

@mod_idsrentry.route('/')
@login_required
def idsrentry():
    """
    Redirects to the Step A (Basic information) from the IDSR's form wizard.
    :returns: the html template for Step A
    """
    url = url_for('idsrentry.step', step='a')
    return redirect(url)

@mod_idsrentry.route('/<step>', methods=['GET', 'POST'])
@login_required
def step(step):
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
    :returns: the html of the form for the passed in step
    """
    fstep = format(step)
    form = newIdsrEntryForm(step)
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
    urltemplate = 'idsrentry/index.html'
    return render_template(urltemplate, form=form, steps=getAvailableSteps())
