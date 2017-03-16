from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from accelidsr.mod_idsrentry.models import save
from accelidsr.mod_idsrentry.models.idsr import Idsr
from accelidsr.mod_idsrentry.forms import getAvailableSteps
from accelidsr.mod_idsrentry.forms import newIdsrEntryForm
from accelidsr.mod_idsrentry.forms import loadIdsrEntryForm

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
    idsrobj = Idsr()
    # Is this a post and form submission?
    if request.method == 'POST':
        # Get the form that suits with the current step, loaded
        # with the vars from request.form
        form = loadIdsrEntryForm(reqform=request.form)
        if form.validate():
            # Seems the data is correct. Get the Idsr object filled
            # with the post data and try to save
            formdict = form.getDict()
            objid = formdict.get('_id','')
            idsrobj = idsrobj if not objid else Idsr.fetch(objid)
            if idsrobj:
                idsrobj.update(formdict)
                if save(idsrobj):
                    flash('Saved!')
                    #TODO Redirect to next step?
                    url = url_for('idsrentry.step', step=step)
                    return redirect(url)

        # Oops, unable to save the form
        flash('Cannot save!')
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
            flash("No IDSR Form found")
            url = url_for('idsrentry.step', step=step)
            return redirect(url)

    # Get the suitable form in accordance with the step
    form = newIdsrEntryForm(idsrobj, step)

    # Render the Html template
    urltemplate = 'idsrentry/index.html'
    return render_template(urltemplate, form=form, steps=getAvailableSteps())
