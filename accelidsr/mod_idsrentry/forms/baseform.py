from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from accelidsr.mod_idsrentry.models.idsr import Idsr
from accelidsr.mod_idsrentry.forms import getPrevStepId as prevstep
from accelidsr.mod_idsrentry.forms import getNextStepId as nextstep
from accelidsr.mod_idsrentry.forms import getStepIds
from accelidsr.mod_idsrentry.forms import getStepTitle
from accelidsr.mod_idsrentry.forms import getAvailableSubsteps


class AbstractIdsrEntryStepForm(FlaskForm):
    """
    Base Form that provides common methods for IDSR forms
    """
    step = ''
    substep = ''
    idsrobj = None
    stepform = HiddenField('')
    substepform = HiddenField('')
    idobj = HiddenField('')
    submit = SubmitField("Next")

    def __init__(self, *args, **kwargs):
        self.step, self.substep = getStepIds(self.__class__.__name__)
        super(AbstractIdsrEntryStepForm, self).__init__(*args, **kwargs)
        self.stepform.data = self.step
        self.substepform.data = self.substep

    def initFromIdsrObject(self, idsrobj=None):
        """
        Fills the fields of the current form in accordance with the Idsr object
        passed in. If no idsrbj is passed, initializes the form with Default
        values.

        :param idsrobj: The Idsr object that will be used to set the values of
            the form fields
        :type idsrobj: accelidsr.mod_idsrentry.models.idsr
        """
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
        self.idsrobj = idsrobj
        self.stepform.data = self.step
        self.substepform.data = self.substep

    def initDefaults(self):
        """
        Initializes the fields of the current form with default values.
        """
        substeps = self.getSubsteps()
        for s in substeps:
            for field in s:
                field.data = field.default
        self.stepform.data = self.step
        self.substepform.data = self.substep
        self.idsrobj = None
        #raise NotImplementedError("Not implemented 'initDefaults(idsrobj)'")

    def getFields(self):
        return [v for k,v in self._fields.items()]

    # TODO: Remove
    def getSubsteps(self):
        """
        Returns a list of lists with the html controls to be rendered for each
        substep of the current form. The list is sorted ascending, so the first
        item of the list (index=0) is the list of html fields to be rendered in
        the substep number 1

        :returns: A 2-tuple with the fields to be rendered in the current form
        :rtype: List of Lists
        """
        #omit = ['idobj', 'stepform', 'substepform', 'submit', 'csrf_token']
        return [[v for k,v in self._fields.items()]]

    def getSubstepIds(self):
        return (sorted(getAvailableSubsteps(self.step).keys()))

    def getStepTitle(self):
        """
        Returns the title of the current step from the IDSR Form

        :returns: the title of the current step
        :rtype: string
        """
        return getStepTitle(self.step)

    def getIdsrObject(self):
        return self.idsrobj

    def getDict(self, idsr_object=None):
        idsrobj = self.idsrobj if not idsr_object else idsr_object
        kvals = {}
        substeps = self.getSubsteps()
        fields = []
        for s in substeps:
            for field in s:
                kvals[field.name] = field.data
        kvals['_id'] = self.idobj.data
        status = 'idsr-status-{0}'.format(self.step)
        substatus = 'idsr-status-{0}_{1}'.format(self.step, self.substep)
        iscomplete = self.isComplete()
        kvals[substatus] = 'complete' if iscomplete else 'incomplete'
        # Now, try to infere the top-level step status
        if idsrobj:
            incomplete = False
            substepids = self.getSubstepIds()
            objdict = idsrobj.getDict()
            for s in substepids:
                if s == self.substep:
                    continue
                key = 'idsr-status-{0}_{1}'.format(self.step, self.substep)
                completed = objdict.get(key, '')
                if completed != 'complete':
                    incomplete = True
                    break
            if incomplete:
                incomplete = True
            elif not iscomplete:
                incomplete = True
            kvals[status] = 'incomplete' if incomplete else 'complete'
        else:
            kvals[status] = 'incomplete'
        return kvals

    def getPrevStepId(self):
        return prevstep(self.step, self.substep)

    def getNextStepId(self):
        return nextstep(self.step, self.substep)

    def isFirstStep(self):
        pstep = self.getPrevStepId()
        return not pstep

    def isLastStep(self):
        nstep = self.getNextStepId()
        return not nstep

    def isFirstSubstep(self):
        pstep = self.getPrevStepId()
        return not pstep or pstep.split('_')[0].lower() != self.step.lower()

    def isLastSubstep(self):
        nstep = self.getNextStepId()
        return not nstep or nstep.split('_')[0].lower() != self.step.lower()

    def isComplete(self):
        miss = [f for f in self.getFields() if f.flags.required and not f.data]
        return len(miss) == 0
