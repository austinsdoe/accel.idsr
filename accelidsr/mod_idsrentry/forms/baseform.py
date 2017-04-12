from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from accelidsr.mod_idsrentry.models.idsr import Idsr
from accelidsr.mod_idsrentry.forms import getPrevStepId as prevstep
from accelidsr.mod_idsrentry.forms import getNextStepId as nextstep
from accelidsr.mod_idsrentry.forms import getStepIds
from accelidsr.mod_idsrentry.forms import getStepTitle
from accelidsr.mod_idsrentry.forms import getAvailableSteps
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
        if not idsrobj or not idsrobj.getDict():
            self.initDefaults()
            return
        for field in self.getFields():
            objval = idsrobj.get(field.name, '')
            field.data = objval if objval else field.data
        if idsrobj.getId():
            self.idobj.data = idsrobj.getId()
        self.idsrobj = idsrobj
        self.stepform.data = self.step
        self.substepform.data = self.substep
        formdict = self.getDict(idsrobj)
        self.idsrobj.update(formdict)

    def initDefaults(self):
        """
        Initializes the fields of the current form with default values.
        """
        for field in self.getFields():
            field.data = field.default
        self.stepform.data = self.step
        self.substepform.data = self.substep
        self.idsrobj = None

    def getFields(self):
        """
        Return a list with the fields (html controls to be rendered) in the
        current form, not sorted.
        :returns: The list of fields to be rendered
        :rtype: list
        """
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
        """
        Returns the ids of the substeps associated to the same step to which
        the current (substep) form is attached, sorted asc.
        As an example, if the current substep is A.1, this function will
        return as many substeps as the top-level step A has: A.1, A.2, A.3,...

        :returns: Substeps associated to the step to which the current form
            belongs to.
        :rtype: A list
        """
        return (sorted(getAvailableSubsteps(self.step).keys()))

    def getStepTitle(self):
        """
        Returns the title of the current step from the IDSR Form

        :returns: the title of the current step
        :rtype: string
        """
        return getStepTitle(self.step)

    def setIdsrObject(self, idsrobject):
        self.idsrobj = idsrobject

    def getIdsrObject(self):
        return self.idsrobj

    def _infereStatus(self, kvals={}):
        status = 'idsr-status-{0}'.format(self.step)
        substatus = 'idsr-status-{0}_{1}'.format(self.step, self.substep)
        if not self.isComplete():
            # If this substep is not complete, then we assume that the whole
            # top-level step will be in an incompleted state too
            kvals[substatus] = 'incomplete'
            kvals[status] = 'incomplete'
            return kvals

        kvals[substatus] = 'complete'

        # At this point, the current sub-step is ok and other sub-steps might
        # been filled previously, so we need to ensure the top-level status is
        # consistent with the rest of sub-steps statuses
        incompleted = 0
        substepids = self.getSubstepIds()
        for s in substepids:
            if s == self.substep:
                # This is the current substep, omit
                continue
            key = 'idsr-status-{0}_{1}'.format(self.step, s)
            if kvals.get(key, '') != 'complete':
                # One sub-step found in an incomplete state, that's enough
                kvals[status] = 'incomplete'
                return kvals

        # All checks passed. Assume the status for the top-level step is
        # complete
        kvals[status] = 'complete'

        bs = kvals.get('bika-status', '')
        if bs and bs in ['failed', 'inserted']:
            return kvals

        # Now, try to establish the status for the whole idsr, with all the
        # steps included, suitable for being submitted to bika
        for s in getAvailableSteps():
            stepstatus = 'idsr-status-{0}'.format(s.get('id','')).lower()
            sstat = kvals.get(stepstatus, '')
            if sstat != 'complete':
                kvals['idsr-status'] = 'incomplete'
                kvals['bika-status'] = 'pending'
                return kvals

        kvals['idsr-status'] = 'complete'
        # TODO If we don't want automatic submission of ARs into Bika, comment
        kvals['bika-status'] = 'in_queue'
        return kvals

    def getDict(self, idsr_object=None):
        idsrobj = self.idsrobj if not idsr_object else idsr_object
        kvals = idsrobj.getDict().copy() if idsrobj else {}
        kvals['_id'] = self.idobj.data

        # We need to fill the value-text fields with both information, so
        # we can use later the text rather than the value to display the info
        # in lists. Example. The value for HealthFacility field corresponds to
        # the uid from Bika instance, but although the text will not be
        # submitted to the Bika instance, we also need it to display it later
        # in lists as human-readable without the need to querying the db
        valuedfields = ['RadioField', 'SelectField']
        for field in self.getFields():
            kvals[field.name] = field.data
            if field.type in valuedfields:
                seltext = [choice[1] for choice in field.choices \
                           if choice[0]==field.data]
                seltext = seltext[0] if (seltext and field.data) else ''
                kvals[field.name+'_text'] = seltext

        # We try to infere the top-level step status and the whole IDSR form
        # status in order to establish the status for the current substep, for
        # the current step and for the whole IDSR form (including other steps)
        self._infereStatus(kvals)
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
        miss = [f for f in self.getFields() if f.flags.required \
                and not str(f.data).strip()]
        return len(miss) == 0

    def stringify(self, choices):
        return '|'.join([c[0] for c in choices if c[0]])
