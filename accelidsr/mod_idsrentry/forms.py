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
    diagnosis_or_condition = SelectField('Diagnosis or Condition', choices=getDiagnosisChoices(), validators=[DataRequired(), ])
    other_diagnosis = TextField('Other diagnosis')

    def getSubsteps(self):
        return [
            [self.diagnosis_or_condition, self.other_diagnosis],
        ]

class IdsrEntryStepCForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    step = 'C'

    # Step C.1
    patient_firstname = TextField('Patient First Name', validators=[DataRequired(), Length(min=3)])
    patient_middlename = TextField('Patient Middle Name')
    patient_lastname = TextField('Patient Last Name', validators=[DataRequired(), Length(min=3)])
    patient_sex = RadioField('Patient Sex',  default='u', choices=[('u', 'Unknown'), ('m', 'Male'), ('f', 'Female')])
    patient_dateofbirth = DateField('Date of Birth', format='%d/%m/%Y', validators=[DataRequired(), ])

    # Step C.2
    patient_county_of_residence = SelectField('County of Residence', choices=getCountiesChoices(), validators=[DataRequired(), ])
    patient_district_of_residence = SelectField('District of Residence', choices=getDistrictChoices(), validators=[DataRequired(), ])
    patient_community_of_residence = TextField('Community of Residence', validators=[DataRequired(), Length(min=3)])

    # Step C.3
    patient_head_of_household = TextField('Head of Household')
    patient_parents_name = TextField('Patient Parents Name')
    patient_phone_number = TextField('Patient Phone Number', validators=[Length(max=10), ])

    # Step C.4
    patient_cross_border = RadioField('Cross Border in Last Month?',  default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])
    patient_case_detected_community = RadioField('Case Detected at Community Level?', default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])


    def getSubsteps(self):
        return [
            [self.patient_firstname, self.patient_middlename, self.patient_lastname, self.patient_sex, self.patient_dateofbirth],
            [self.patient_county_of_residence, self.patient_district_of_residence, self.patient_community_of_residence],
            [self.patient_head_of_household, self.patient_parents_name, self.patient_phone_number],
            [self.patient_cross_border, self.patient_case_detected_community]
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
