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
from accelidsr.mod_idsrentry.models import save
from flask_login import current_user

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


@mod_dashboard.route('/doaction', methods=['POST'])
@login_required
def doaction():
    """
    Handles actions for idsr lists from forms submitted on Dashboard.
    Calls a method depending on Action and displays the message.
    """
    url = '/'
    message = ''
    category = 'info'
    fdict = request.form.to_dict()
    try:
        action = fdict.get('action')
        ids = request.form.getlist('chk_idsr_ids')
        if action == 'Cancel':
            message = _cancel_idsrs(ids)
    except:
        message = 'An error occured...'
        category = 'error'
    flash(message, category=category)
    url = url_for('dashboard.idsrlist')
    return redirect(url)


def _cancel_idsrs(ids):
    """
    Sets 'bika-status' of IDSR Forms to 'cancelled' according to given IDs.
    Forms can be cancelled only if they are 'in_queue' state. Thus, returns
    message containing numbers of cancelled, skipped and failed operations.

    :param ids: list of unique IDs of IDSR Forms
    :type func: list
    """
    n_cancelled = 0
    n_skipped = 0
    n_failed = 0
    for i in ids:
        try:
            idsrobj = Idsr.fetch(i)
            status = idsrobj.getDict().get('bika-status')
            if not status == 'in_queue':
                n_skipped += 1
                continue
            idsrobj.update({"bika-status": "cancelled",
                            "modifiedby": current_user.get_username()})
            if not save(idsrobj):
                n_failed += 1
                continue
            n_cancelled += 1
        except:
            n_failed += 1

    return 'Cancelled: %d , Skipped: %d , Failed: %d' % (n_cancelled,
                                                         n_skipped, n_failed)
