from wtforms import StringField, BooleanField, RadioField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired
from accelidsr.mod_partialidsr.forms import registerStepForm
from accelidsr.mod_partialidsr.forms.baseform import AbstractPartialIdsrStepForm

STEP = ('C', 'Patient Information')


class PartialIdsrC(AbstractPartialIdsrStepForm):
    """
    Partial Form "Step C- Patient Information".
    """
    patient_anonymous = BooleanField(
        'Anonymous Patient')

    patient_firstname = StringField(
        'Patient First Name',
        validators=[InputRequired(), Length(min=3)])

    patient_middlename = StringField(
        'Patient Middle Name')

    patient_lastname = StringField(
        'Patient Last Name',
        validators=[InputRequired(), Length(min=3)])

    patient_client_patientid = StringField(
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
        Validator function of C step.
        """
        success = super(PartialIdsrC, self).validate()
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

registerStepForm(clazz=PartialIdsrC, step=STEP)
