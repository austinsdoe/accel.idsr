from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateField, SelectField, \
                    SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import Form
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry import getFacilityChoices
from accelidsr.mod_idsrentry import getDiagnosisChoices

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
        return IdsrEntryStepAForm()
    if step.lower() == 'b':
        return IdsrEntryStepBForm()
    if step.lower() == 'c':
        return IdsrEntryStepCForm()
    if step.lower() == 'd':
        return IdsrEntryStepDForm()
    raise NotImplementedError("No form available for step '%s'" % step)


class AbstractIdsrEntryStepForm(Form):
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


class IdsrEntryStepAForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step A - Basic Information" from IDSR Form.
    """
    step = 'A'

    # Step A.1
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step A.2
    reporting_country = SelectField('Reporting Country', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = SelectField('Reporting District', choices=getDistrictChoices(), validators=[DataRequired(), ])
    facility_name = SelectField('Health Facility Name', choices=getFacilityChoices(), validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.reporting_date, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]

class IdsrEntryStepBForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step B - Diagnosis information" from IDSR Form.
    """
    step = 'B'

    # Step B.1
    diagnosis_or_condition = RadioField('Diagnosis or Condition', choices=getDiagnosisChoices(), validators=[DataRequired(), ])
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step B.2
    reporting_country = SelectField('Reporting County', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = SelectField('Reporting District', choices=getDistrictChoices(), validators=[DataRequired(), ])
    facility_name = SelectField('Health Facility Name', choices=getFacilityChoices(), validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.diagnosis_or_condition, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]

class IdsrEntryStepCForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    step = 'C'

    # Step A.1
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step A.2
    reporting_country = SelectField('Reporting Country', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = TextField('Reporting District', validators=[DataRequired(), ])
    facility_name = TextField('Health Facility Name', validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.reporting_date, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]

class IdsrEntryStepDForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step D - Clinical information" from IDSR Form.
    """
    step = 'D'

    # Step A.1
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step A.2
    reporting_country = SelectField('Reporting Country', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = TextField('Reporting District', validators=[DataRequired(), ])
    facility_name = TextField('Health Facility Name', validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.reporting_date, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]
