from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateField, SelectField, \
                    SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry.forms import registerStepForm
from accelidsr.mod_idsrentry.forms.baseform import AbstractIdsrEntryStepForm

STEP = ('C', 'Patient Basic information')


class IdsrEntryStepC1Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    patient_anonymous = BooleanField('Anonymous Patient')
    patient_firstname = TextField('Patient First Name', validators=[DataRequired(), Length(min=3)])
    patient_middlename = TextField('Patient Middle Name')
    patient_lastname = TextField('Patient Last Name', validators=[DataRequired(), Length(min=3)])
    patient_client_patientid = TextField('Client Patient ID', validators=[DataRequired(), Length(min=3)])
    patient_gender = RadioField('Patient Gender',  default='u', choices=[('u', 'Unknown'), ('m', 'Male'), ('f', 'Female')])
    patient_dateofbirth = DateField('Date of Birth', format='%d/%m/%Y', validators=[DataRequired(), ])
    patient_age_years = IntegerField('Patient Age. Years', validators=[DataRequired(),])
    patient_age_months = IntegerField('Patient Age. Months', validators=[DataRequired(),])
    patient_age_days = IntegerField('Patient Age. Days', validators=[DataRequired(),])

registerStepForm(clazz=IdsrEntryStepC1Form, step=STEP, substep=1)


class IdsrEntryStepC2Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    patient_county_of_residence = SelectField('Patient County of Residence', choices=getCountiesChoices(), validators=[DataRequired(), ])
    patient_district_of_residence = SelectField('Patient District of Residence', choices=getDistrictChoices(), validators=[DataRequired(), ])
    patient_community_of_residence = TextField('Patient Community of Residence', validators=[DataRequired(), Length(min=3)])

registerStepForm(clazz=IdsrEntryStepC2Form, step=STEP, substep=2)


class IdsrEntryStepC3Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    # Step C.3
    patient_head_of_household = TextField('Head of Household')
    patient_parents_name = TextField('Parents Name (if young)')
    patient_phone_number = TextField('Parent Phone Number', validators=[Length(max=10), ])

registerStepForm(clazz=IdsrEntryStepC3Form, step=STEP, substep=3)


class IdsrEntryStepC4Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    # Step C.4
    patient_cross_border = RadioField('Cross Border in Last Month?',  default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])
    patient_case_detected_community = RadioField('Case Detected at Community Level?', default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])

registerStepForm(clazz=IdsrEntryStepC4Form, step=STEP, substep=4)
