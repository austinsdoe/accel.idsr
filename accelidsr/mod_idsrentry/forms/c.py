from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateTimeField, SelectField, \
                    SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Email, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry.forms import registerStepForm
from accelidsr.mod_idsrentry.forms.baseform import AbstractIdsrEntryStepForm
from accelidsr.mod_idsrentry.validators import DynamicDataValidator

STEP = ('C', 'Patient Basic information')


class IdsrEntryStepC1Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    patient_anonymous = BooleanField(
        'Anonymous Patient')

    patient_firstname = TextField(
        'Patient First Name',
        validators=[InputRequired(), Length(min=3)])

    patient_middlename = TextField(
        'Patient Middle Name')

    patient_lastname = TextField(
        'Patient Last Name',
        validators=[InputRequired(), Length(min=3)])

    patient_client_patientid = TextField(
        'Patient Record ID',
        validators=[InputRequired(), Length(min=3)])

    patient_gender = RadioField(
        'Patient Gender',
        default='dk',
        choices=[('dk', 'Unknown'), ('male', 'Male'), ('female', 'Female')])

    patient_birth_date_estimated = BooleanField(
        'Date of Birth is estimated (years)')

    patient_dateofbirth = DateTimeField(
        'Date of Birth',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'input-type': 'date'})

    patient_age_years = IntegerField(
        'Patient Age. Years',
        validators=[InputRequired(), ])

    patient_age_months = IntegerField(
        'Patient Age. Months',
        validators=[InputRequired(), ])

    patient_age_days = IntegerField(
        'Patient Age. Days',
        validators=[InputRequired(), ])

    def validate(self):
        """
        Validator function of C1 step.
        Adds an error message and returns False if any field fails to be saved.
        """
        success = super(IdsrEntryStepC1Form, self).validate()
        failures = 0 if success else 1
        objdict = self.getDict()

        # Checking if Date of Birth is correct. Since DateTimeField already
        # has a date formatter, it returns None when entered value is not in
        # proper format. Just adding error message here.
        dof = self.patient_dateofbirth.data
        if not dof:
            self.patient_dateofbirth.errors.append(" Please enter valid Date \
            of Birth in DD/MM/YYYY format.")
            failures += 1

        return failures == 0


registerStepForm(clazz=IdsrEntryStepC1Form, step=STEP, substep=1)


class IdsrEntryStepC2Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    patient_county_of_residence = SelectField(
        'Patient County of Residence',
        choices=getCountiesChoices(),
        validators=[DataRequired(), ])

    patient_district_of_residence = SelectField(
        'Patient District of Residence',
        choices=getDistrictChoices(),
        validators=[DataRequired(), DynamicDataValidator(), ],)

    patient_community_of_residence = TextField(
        'Patient Community of Residence',
        validators=[DataRequired(), Length(min=3)])

    def initFromIdsrObject(self, idsrobj=None):
        super(IdsrEntryStepC2Form, self).initFromIdsrObject(idsrobj)
        # We need first to assign the choices to fields their values are
        # rendered dynamically
        county = self.patient_county_of_residence.data
        district = self.patient_district_of_residence.data
        districts = getDistrictChoices(county)
        self.patient_district_of_residence.choices = districts

registerStepForm(clazz=IdsrEntryStepC2Form, step=STEP, substep=2)


class IdsrEntryStepC3Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    # Step C.3
    patient_head_of_household = TextField('Head of Household')
    patient_parents_name = TextField('Parents Name (if young)')
    patient_phone_number = TextField('Contact Phone Number', validators=[Length(max=10), ])

registerStepForm(clazz=IdsrEntryStepC3Form, step=STEP, substep=3)


class IdsrEntryStepC4Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    # Step C.4
    patient_cross_border = RadioField('Cross Border in Last Month?',  default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])
    patient_case_detected_community = RadioField('Case Detected at Community Level?', default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])

registerStepForm(clazz=IdsrEntryStepC4Form, step=STEP, substep=4)
