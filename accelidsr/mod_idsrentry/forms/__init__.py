from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from accelidsr.mod_idsrentry.models.idsr import Idsr

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

def loadIdsrEntryForm(reqform):
    if reqform is None:
        raise NotImplementedError("No form object passed in")

    step = reqform.get('formstep')
    if step.lower() == 'a':
        from accelidsr.mod_idsrentry.forms.a import IdsrEntryStepAForm
        form = IdsrEntryStepAForm(reqform)
    elif step.lower() == 'b':
        from accelidsr.mod_idsrentry.forms.b import IdsrEntryStepBForm
        form = IdsrEntryStepBForm(reqform)
    elif step.lower() == 'c':
        from accelidsr.mod_idsrentry.forms.c import IdsrEntryStepCForm
        form =  IdsrEntryStepCForm(reqform)
    elif step.lower() == 'd':
        from accelidsr.mod_idsrentry.forms.d import IdsrEntryStepDForm
        form =  IdsrEntryStepDForm(reqform)
    else:
        raise NotImplementedError("No form available for step '%s'" % step)
    return form

def newIdsrEntryForm(idsrobj=None, step='a'):
    """
    Returns the Form to be loaded in accordance with the step passed in.
    If there is no defined form for the step passed in, throws an Error.

    :param step: The step identifier from the IDSR Form
    :type step: string
    :param idsrobj: The Idsr object to attach to the current form
    :type id: string
    :returns: A form for the step passed in
    :rtype: AbstractIdsrEntryStepForm
    """
    if step is None:
        raise NotImplementedError("No step passed in")

    form = None
    if step.lower() == 'a':
        from accelidsr.mod_idsrentry.forms.a import IdsrEntryStepAForm
        form = IdsrEntryStepAForm()
    elif step.lower() == 'b':
        from accelidsr.mod_idsrentry.forms.b import IdsrEntryStepBForm
        form = IdsrEntryStepBForm()
    elif step.lower() == 'c':
        from accelidsr.mod_idsrentry.forms.c import IdsrEntryStepCForm
        form = IdsrEntryStepCForm()
    elif step.lower() == 'd':
        from accelidsr.mod_idsrentry.forms.d import IdsrEntryStepDForm
        form = IdsrEntryStepDForm()
    else:
        raise NotImplementedError("No form available for step '%s'" % step)

    form.initFromIdsrObject(idsrobj)
    return form


class AbstractIdsrEntryStepForm(FlaskForm):
    """
    Base Form that provides common methods for IDSR forms
    """
    step = ''
    idobj = HiddenField('')
    formstep = HiddenField('')
    submit = SubmitField("Next")

    def initFromIdsrObject(self, idsrobj=None):
        """
        Fills the fields of the current form in accordance with the Idsr object
        passed in. If no idsrbj is passed, initializes the form with Default
        values.

        :param idsrobj: The Idsr object that will be used to set the values of
            the form fields
        :type idsrobj: accelidsr.mod_idsrentry.models.idsr
        """
        self.formstep.data = self.step
        if idsrobj is None:
            self.initDefaults()
            return

        substeps = self.getSubsteps()
        for s in substeps:
            for field in s:
                objval = idsrobj.get(field.name,'')
                field.data = objval if objval else field.data
        if idsrobj.getId():
            self.idobj.data = idsrobj.getId()

    def initDefaults(self):
        """
        Initializes the fields of the current form with default values.
        """
        substeps = self.getSubsteps()
        for s in substeps:
            for field in s:
                field.data = field.default
        #raise NotImplementedError("Not implemented 'initDefaults(idsrobj)'")

    def getSubsteps(self):
        """
        Returns a list of lists with the html controls to be rendered for each
        substep of the current form. The list is sorted ascending, so the first
        item of the list (index=0) is the list of html fields to be rendered in
        the substep number 1

        :returns: A 2-tuple with the fields to be rendered in the current form
        :rtype: List of Lists
        """
        raise NotImplementedError("Not implemented 'getSubsteps(idsrobj)'")

    def getStepTitle(self):
        """
        Returns the title of the current step from the IDSR Form

        :returns: the title of the current step
        :rtype: string
        """
        return getStepTitle(self.step)

    def getDict(self):
        kvals = {}
        substeps = self.getSubsteps()
        fields = []
        for s in substeps:
            for field in s:
                kvals[field.name] = field.data
        kvals['_id'] = self.idobj.data
        return kvals
