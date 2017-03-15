from flask_wtf import FlaskForm
from wtforms import SubmitField

def getAvailableSteps():
    """
    Returns the available steps for the IDSR Form
    :returns: a list of dicts, sorted asc. Each dict with the following keys:
        id, title
    :rtype: list of dicts
    """
    return [
        {'id': 'a', 'title': 'Basic information'},
        {'id': 'b', 'title': 'Diagnosis information'},
        {'id': 'c', 'title': 'Patient Basic information'},
        {'id': 'd', 'title': 'Clinical information'},
    ]

def getStepTitle(step):
    """
    Returns the title for the step passed in
    :param step: The step identifier from the IDSR Form
    :type step: string
    :returns: The title of the step
    :rtype: string
    """
    steps = getAvailableSteps()
    title = [s['title'] for s in steps if s['id'] == step]
    if len(title) == 1:
        return title[0]
    return ''

def newIdsrEntryForm(step):
    """
    Returns the Form to be loaded in accordance with the step passed in.
    If there is no defined form for the step passed in, throws an Error.

    :param step: The step identifier from the IDSR Form
    :type step: string
    :returns: A form for the step passed in
    :rtype: AbstractIdsrEntryStepForm
    """
    if step.lower() == 'a':
        from accelidsr.mod_idsrentry.forms.a import IdsrEntryStepAForm
        return IdsrEntryStepAForm()
    if step.lower() == 'b':
        from accelidsr.mod_idsrentry.forms.b import IdsrEntryStepBForm
        return IdsrEntryStepBForm()
    if step.lower() == 'c':
        from accelidsr.mod_idsrentry.forms.c import IdsrEntryStepCForm
        return IdsrEntryStepCForm()
    if step.lower() == 'd':
        from accelidsr.mod_idsrentry.forms.d import IdsrEntryStepDForm
        return IdsrEntryStepDForm()
    raise NotImplementedError("No form available for step '%s'" % step)


class AbstractIdsrEntryStepForm(FlaskForm):
    """
    Base Form that provides common methods for IDSR forms
    """
    step = ''

    submit = SubmitField("Next")

    def getSubsteps(self):
        """
        Returns a list of lists with the html controls to be rendered for each
        substep of the current form. The list is sorted ascending, so the first
        item of the list (index=0) is the list of html fields to be rendered in
        the substep number 1

        :returns: A 2-tuple with the fields to be rendered in the current form
        :rtype: List of Lists
        """
        raise NotImplementedError("Should have implemented this")

    def getStepTitle(self):
        """
        Returns the title of the current step from the IDSR Form

        :returns: the title of the current step
        :rtype: string
        """
        return getStepTitle(self.step)
