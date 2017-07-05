from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from accelidsr.mod_idsrentry.models import save
from accelidsr.mod_idsrentry.models.idsr import Idsr
from accelidsr.mod_partialidsr.forms import getAvailableSteps
from accelidsr.mod_partialidsr.forms import newStepFormInstance
from accelidsr.mod_partialidsr.forms import loadStepFormInstance

# Define the blueprint: 'partialidsr', set its url prefix: app.url/partialidsr
mod_partialidsr = Blueprint('partialidsr', __name__, url_prefix='/partialidsr')


@mod_partialidsr.route('/')
@login_required
def partialidsrentry():
    """
    Redirects to the Step A (Basic information) from the Partial IDSR's form wizard.
    :returns: the html template for Step A
    """
    url = url_for('partialidsr.step', step='a')
    return redirect(url)

@mod_partialidsr.route('/<step>', methods=['GET', 'POST'])
@login_required
def step(step):
    """
    Renders Partial form as same as Full IDSR Form under 'mod_idsrentry.controllers.step' does. The difference is that
    we don't have substeps here.

    :param step: the step (and/or substep) to load (e.g 'a', 'b_2')
    :param type: string
    :returns: the html of the form for the passed in step (and/or substep)
    """
    idsrobj = Idsr()
    if request.method == 'POST':
        form = loadStepFormInstance(requestform=request.form)
        fdict = request.form.to_dict()
        for field in form:
            dname = field.name + '_dynamic'
            if field.type == "SelectField" and dname in fdict:
                choices = fdict.get(dname)
                field.choices = [(c, fdict.get(field.name+'_text', c)) for c in choices.split('|')]
        if form.validate():
            # Seems the data is correct. Get the Idsr object filled
            # with the post data and try to save
            fidsr = form.getIdsrObject()
            if fidsr:
                idsrobj = fidsr
            formdict = form.getDict(idsrobj)
            if not idsrobj.getId():
                formdict['createdby'] = current_user.get_username()
                formdict['is_partial'] = True
            formdict['modifiedby'] = current_user.get_username()
            idsrobj.update(formdict)
            if save(idsrobj):
                nextstep = form.getNextStepId()
                if nextstep:
                    url = url_for('partialidsr.step',
                                  step=nextstep,
                                  id=idsrobj.getId())
                    return redirect(url)
                else:
                    # This is the last step. Redirect to preview page
                    return redirect(url_for('partialidsr.preview',
                                            id=idsrobj.getId()))

        # Oops, unable to save the form
        message = 'Cannot save!'
        flash(message, category='error')

        urltemplate = 'idsrentry/index.html'
        return render_template(urltemplate, form=form,
                               steps=getAvailableSteps(), is_partial=True)

    # No Post submission, check if this is a previously created IDSR record
    id = request.args.get('id')
    if id:
        idsrobj = Idsr.fetch(id)
        if idsrobj:
            #TODO Check the user has enough privileges if previously data is available
            pass
        else:
            flash("No IDSR Form found", category='error')
            url = url_for('partialidsr.step', step=step)
            return redirect(url)

    # Get the suitable form in accordance with the step
    form = newStepFormInstance(step)
    form.initFromIdsrObject(idsrobj)

    # Render the Html template
    urltemplate = 'idsrentry/index.html'
    return render_template(urltemplate, form=form, steps=getAvailableSteps(), is_partial=True)


@mod_partialidsr.route('/preview', methods=['GET', 'POST'])
@login_required
def preview():
    id = request.args.get('id')
    if not id:
        return render_template('404.html'), 404
    idsrobj = Idsr.fetch(id)
    if not idsrobj:
        return render_template('404.html'), 404

    urltemplate = 'idsrentry/preview.html'
    return render_template(urltemplate, idsrobj=idsrobj)


@mod_partialidsr.route('/submit', methods=['POST'])
@login_required
def submit():
    id = request.form.get('id')
    if not id:
        return render_template('404.html'), 404
    idsrobj = Idsr.fetch(id)
    if not idsrobj:
        return render_template('404.html'), 404

    kvals = idsrobj.getDict().copy()
    if not kvals.get('idsr-status') == 'complete':
        return render_template('404.html'), 404

    kvals['bika-status'] = 'in_queue'
    idsrobj.update(kvals)
    if save(idsrobj):
        message = 'Form Submitted!'
        flash(message, category='info')
        return redirect(url_for('index'))

    # It was already in_queue state, nothing to do
    message = 'Form has been submitted before.'
    flash(message, category='info')
    return redirect(url_for('index'))
