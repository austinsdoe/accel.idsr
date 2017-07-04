from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from accelidsr.mod_partialidsr.forms import getPrevStepId as prevstep
from accelidsr.mod_partialidsr.forms import getNextStepId as nextstep
from accelidsr.mod_partialidsr.forms import getStepIds
from accelidsr.mod_partialidsr.forms import getStepTitle
from accelidsr.mod_partialidsr.forms import getAvailableSteps


class AbstractPartialIdsrStepForm(FlaskForm):
    """
    Base Form that provides common methods for Partial IDSR forms
    """
    step = ''
    idsrobj = None
    stepform = HiddenField('')
    idobj = HiddenField('')
    submit = SubmitField("Next")

    def __init__(self, *args, **kwargs):
        self.step = getStepIds(self.__class__.__name__)
        super(AbstractPartialIdsrStepForm, self).__init__(*args, **kwargs)
        self.stepform.data = self.step

    def initFromIdsrObject(self, idsrobj=None):
        """
        Fills the fields of the current form in accordance with the Idsr object
        passed in. If no idsrobj is passed, initializes the form with Default
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
        formdict = self.getDict(idsrobj)
        self.idsrobj.update(formdict)

    def initDefaults(self):
        """
        Initializes the fields of the current form with default values.
        """
        for field in self.getFields():
            field.data = field.default
        self.stepform.data = self.step
        self.idsrobj = None

    def getFields(self):
        """
        Return a list with the fields (html controls to be rendered) in the
        current form, not sorted.
        :returns: The list of fields to be rendered
        :rtype: list
        """
        return [v for k,v in self._fields.items()]

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
        if not self.isComplete():
            kvals[status] = 'incomplete'
            return kvals

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
        return prevstep(self.step)

    def getNextStepId(self):
        return nextstep(self.step)

    def isFirstStep(self):
        pstep = self.getPrevStepId()
        return not pstep

    def isLastStep(self):
        nstep = self.getNextStepId()
        return not nstep

    def isComplete(self):
        miss = [f for f in self.getFields() if f.flags.required \
                and str(f.data).strip() == 'None']
        return len(miss) == 0

    def stringify(self, choices):
        return '|'.join([c[0] for c in choices if c[0]])

    def isPartialIdsr(self):
        return True
