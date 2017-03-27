from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from accelidsr.mod_idsrentry.models import save
from accelidsr.mod_idsrentry.models.idsr import Idsr
from accelidsr.mod_idsrentry.json import IdsrJson
from accelidsr.mod_idsrentry.forms import getAvailableSteps
from accelidsr.mod_idsrentry.forms import getNextStepId
from accelidsr.mod_idsrentry.forms import newStepFormInstance
from accelidsr.mod_idsrentry.forms import loadStepFormInstance

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

@mod_idsrentry.route('/@@json/<func>', methods=['GET', 'POST'])
@login_required
def json(func):
    results = {'error': 'Not a valid function'}
    if request.method == 'POST':
        cargs = request.form.to_dict()
        json = IdsrJson()
        results = getattr(json, func)(**cargs)
    return jsonify(results)

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
    idsrobj = Idsr()
    rawstep = step
    tokens = step.split('_')
    step = tokens[0] if tokens else step
    substep = tokens[1] if len(tokens) > 1 else 1
    # Is this a post and form submission?
    if request.method == 'POST':
        # Get the form that suits with the current step, loaded
        # with the vars from request.form
        form = loadStepFormInstance(requestform=request.form)
        # We need first to assign the choices to fields their values have been
        # rendered dynamically to prevent the validation to fail.
        # Used for fields like District SelectField, loaded dynamically when
        # a County is selected in the form.
        # https://wtforms.readthedocs.io/en/latest/fields.html#wtforms.fields.SelectField
        fdict = request.form.to_dict()
        for field in form:
            dname = field.name + '_dynamic'
            if field.type == "SelectField" and dname in fdict:
                choices = fdict.get(dname)
                field.choices = [(c, c) for c in choices.split('|')]
        if form.validate():
            # Seems the data is correct. Get the Idsr object filled
            # with the post data and try to save
            formdict = form.getDict()
            objid = formdict.get('_id','')
            idsrobj = idsrobj if not objid else Idsr.fetch(objid)
            if idsrobj:
                formdict = form.getDict(idsrobj)
                idsrobj.update(formdict)
                if save(idsrobj):
                    nextstep = form.getNextStepId()
                    if nextstep:
                        url = url_for('idsrentry.step', step=nextstep, id=idsrobj.getId())
                        return redirect(url)
                    else:
                        # This is the last step. Redirect to main page
                        return redirect(url_for('index'))

        # Oops, unable to save the form
        message = 'Cannot save!'
        flash(message, category='error')

        urltemplate = 'idsrentry/index.html'
        return render_template(urltemplate, form=form,
            steps=getAvailableSteps())

    # No Post submission, check if this is a previously created IDSR record
    id = request.args.get('id')
    if id:
        # This is a previously created form. Fetch the data stored in the db
        # for this IDSR record, check if the user has enough privileges and
        # fill the form fields with previously stored values
        idsrobj = Idsr.fetch(id)
        if idsrobj:
            #TODO Check the user has enough privileges if previously data is available
            pass
        else:
            flash("No IDSR Form found", category='error')
            url = url_for('idsrentry.step', step=rawstep)
            return redirect(url)

    # Get the suitable form in accordance with the step
    form = newStepFormInstance(step, substep)
    form.initFromIdsrObject(idsrobj)

    # Render the Html template
    urltemplate = 'idsrentry/index.html'
    return render_template(urltemplate, form=form, steps=getAvailableSteps())
